from sqlalchemy.orm import Session
from models import Order, Vehicle, Route
from collections import deque
import heapq
from route import optimal_route  # Import function
import joblib
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import googlemaps

load_dotenv()


# Weather condition mapping
weather_condition_codes = { 
    200: 'Thunderstorm: thunderstorm with light rain', 201: 'Thunderstorm: thunderstorm with rain', 
    202: 'Thunderstorm: thunderstorm with heavy rain', 210: 'Thunderstorm: light thunderstorm', 
    211: 'Thunderstorm: thunderstorm', 212: 'Thunderstorm: heavy thunderstorm', 
    221: 'Thunderstorm: ragged thunderstorm', 230: 'Thunderstorm: thunderstorm with light drizzle', 
    231: 'Thunderstorm: thunderstorm with drizzle', 232: 'Thunderstorm: thunderstorm with heavy drizzle',
    300: 'Drizzle: light intensity drizzle', 301: 'Drizzle: drizzle', 302: 'Drizzle: heavy intensity drizzle', 
    310: 'Drizzle: light intensity drizzle rain', 311: 'Drizzle: drizzle rain', 
    312: 'Drizzle: heavy intensity drizzle rain', 313: 'Drizzle: shower rain and drizzle', 
    314: 'Drizzle: heavy shower rain and drizzle', 321: 'Drizzle: shower drizzle',
    500: 'Rain: light rain', 501: 'Rain: moderate rain', 502: 'Rain: heavy intensity rain', 
    503: 'Rain: very heavy rain', 504: 'Rain: extreme rain', 511: 'Rain: freezing rain', 
    520: 'Rain: light intensity shower rain', 521: 'Rain: shower rain', 522: 'Rain: heavy intensity shower rain', 
    531: 'Rain: ragged shower rain',
    600: 'Snow: light snow', 601: 'Snow: snow', 602: 'Snow: heavy snow', 611: 'Snow: sleet', 
    612: 'Snow: light shower sleet', 613: 'Snow: shower sleet', 615: 'Snow: light rain and snow', 
    616: 'Snow: rain and snow', 620: 'Snow: light shower snow', 621: 'Snow: shower snow', 
    622: 'Snow: heavy shower snow',
    701: 'Mist: mist', 711: 'Smoke: smoke', 721: 'Haze: haze', 731: 'Dust: sand/dust whirls', 
    741: 'Fog: fog', 751: 'Sand: sand', 761: 'Dust: dust', 762: 'Ash: volcanic ash', 
    771: 'Squall: squalls', 781: 'Tornado: tornado',
    800: 'Clear: clear sky', 801: 'Clouds: few clouds (11-25%)', 802: 'Clouds: scattered clouds (25-50%)', 
    803: 'Clouds: broken clouds (51-84%)', 804: 'Clouds: overcast clouds (85-100%)'
}

# Weather factor mapping
weather_factor = { 
    "Thunderstorm": 1.5, "Drizzle": 1.2, "Rain": 1.3, "Snow": 1.7, "Mist": 1.1, "Smoke": 1.2, 
    "Haze": 1.2, "Dust": 1.1, "Fog": 1.2, "Sand": 1.1, "Ash": 1.4, "Squall": 1.5, 
    "Tornado": 2.0, "Clear": 1.0, "Clouds": 1.1
}


class OrderManager:
    def __init__(self, db: Session):
        self.db = db
        # Load ML Model and Preprocessing Components
        with open("ml_models/delivery_time_model (2).pkl", "rb") as f:
            self.model = joblib.load(f)
        with open("ml_models/scaler (2).pkl", "rb") as f:
            self.scaler = joblib.load(f)
        with open("ml_models/label_encoders (2).pkl", "rb") as f:
            self.label_encoders = joblib.load(f)

    def assign_orders(self):
        """Assign PENDING and IN-PROCESS orders to available vehicles and compute optimal routes."""
        order_queue = []
        unassigned_orders = deque()
        assigned_orders = []  # Track assigned orders
        assigned_order_ids = set()  # Prevent duplicate assignments

        # Fetch "pending" and "in-process" orders
        for order in self.db.query(Order).filter(Order.status.in_(["pending", "in-process"])).all():
            heapq.heappush(order_queue, (order.priority, order.id, order))

        # Fetch fresh list of vehicles every time
        vehicles = {v.id: v for v in self.db.query(Vehicle).all()}
        vehicle_loads = {v.id: 0 for v in vehicles.values()}  # Track used capacity

        while order_queue:
            _, order_id, order = heapq.heappop(order_queue)
            
            if order_id in assigned_order_ids:  # Prevent duplicate assignments
                continue  

            assigned = False

            for vehicle in vehicles.values():
                remaining_capacity = vehicle.capacity - vehicle_loads[vehicle.id]
                if remaining_capacity >= order.weight:
                    vehicle_loads[vehicle.id] += order.weight
                    order.vehicle_id = vehicle.id
                    order.status = "in-process"  # Update status to in-process
                    self.db.commit()
                    assigned_orders.append(order)
                    assigned_order_ids.add(order_id)  # Track assigned orders
                    assigned = True
                    break

            if not assigned:
                order.status = "pending"
                order.vehicle_id = None
                order.route_id = None
                self.db.commit()
                unassigned_orders.append(order)

        # Compute routes once assignments are done
        self.compute_routes(assigned_orders, vehicles)

    def get_weather(self, lat, lon):
        """Fetch weather condition and factor based on coordinates."""
        print(lat,lon,type(lat))
        # lat = float(lat)
        # lon = float(lon)
        # print(lat,lon,type(lat))
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.getenv('OPENWEATHERMAP_APIKEY')}"
        print(url)
        try:
            response = requests.get(url).json()
            print(response)

            # Extract weather condition code

            weather_code = response["weather"][0]["id"]
        except:
            weather_code = 800
        weather_condition = weather_condition_codes.get(weather_code, "Unknown")
        weather_category = weather_condition.split(":")[0]  # Extract main category

        # Assign weather factor
        weather_factor_value = weather_factor.get(weather_category, 1.0)

        return weather_condition, weather_factor_value
    def TrafficLevel(self, lat, lon):
        # Initialize Google Maps API client
        gmaps = googlemaps.Client(key=os.getenv('GOOGLEMAP_APIKEY'))
        origin = (19.116458, 72.902696)
        destination = (lat,lon)
        # Get distance matrix with traffic data (departure_time = 'now' to include real-time traffic)
        matrix = gmaps.distance_matrix(
            origin,
            destination,
            departure_time='now',  # 'now' to include real-time traffic data
            traffic_model='best_guess',  # Optional: 'optimistic', 'pessimistic'
            mode='driving'  # Mode of transportation (driving, walking, etc.)
        )
                
        # Extract travel time data
        if matrix['status'] == 'OK':
            element = matrix['rows'][0]['elements'][0]

            if element['status'] == 'OK':
                duration = element['duration']['value']  # in seconds
                duration_in_traffic = element['duration_in_traffic']['value']  # in seconds

                # Calculate percentage increase
                increase_percent = ((duration_in_traffic - duration) / duration) * 100

                # Classify traffic conditions
                if increase_percent <= 0:
                    traffic_condition = 'No Traffic'
                elif increase_percent <= 10:
                    traffic_condition = 'Light'
                elif increase_percent <= 30:
                    traffic_condition = 'Moderate'
                else:
                    traffic_condition = 'Heavy'

                print(f"Duration (Normal): {element['duration']['text']}")
                print(f"Duration (With Traffic): {element['duration_in_traffic']['text']}")
                print(f"Traffic Condition: {traffic_condition}")
            else:
                print(f"Error in response: {element['status']}")
        else:
            print(f"Error in response: {matrix['status']}")

        return traffic_condition
    
    def compute_routes(self, assigned_orders, vehicles):
        """Compute optimal routes for vehicles that received orders."""
        for vehicle in vehicles.values():
            vehicle_orders = [order for order in assigned_orders if order.vehicle_id == vehicle.id]
            
            if not vehicle_orders:
                continue  # Skip if no orders assigned

            # Extract delivery locations & mapping to actual orders
            delivery_locations = []
            order_map = {}  # Maps delivery index → order object

            for idx, order in enumerate(vehicle_orders):
                coords = tuple(map(float, order.delivery_coordinates.split(",")))
                delivery_locations.append(coords)
                order_map[idx] = order  # Map index to order object

            # Compute optimized route and distances
            full_route, optimized_order_indexes, distance = optimal_route(delivery_locations)
            print("------------------------------")
            print(full_route, optimized_order_indexes, distance)
            print("------------------------------")

            if not isinstance(optimized_order_indexes, list):
                raise ValueError(f"Expected list for optimized_order_indexes, got {type(optimized_order_indexes)}: {optimized_order_indexes}")

            # Assign distances to the correct orders
            input_data = []
            assigned_orders_as_per_route = []
            for idx, order_index in enumerate(optimized_order_indexes[1:-1]):  # Skip first warehouse index (0)
                if order_index - 1 in order_map:  # Ensure valid index
                    order = order_map[order_index - 1]
                    order.delivery_distance = distance[idx]  # Assign computed distance
                    assigned_orders_as_per_route.append(order)

                    # Fetch weather data
                    lat, lon = map(str.strip, order.delivery_coordinates.split(","))

                    print("for weather",lat, lon)
                    weather_condition, weather_factor_value = self.get_weather(lat, lon)
                    try:
                        traffic_level = self.TrafficLevel(lat,lon)
                    except:
                        # If problem in traffic API assuming traffic_level
                        traffic_level = "Moderate"

                    # Prepare input for ML Model
                    input_data.append({
                        "Dropoff Latitude": float(lat),
                        "Dropoff Longitude": float(lon),
                        "Total Distance (km)": order.delivery_distance,
                        "Traffic Level": traffic_level,
                        "Stops Before Delivery": idx + 1,
                        "Weather Condition": weather_condition,
                        "Total Processing Time (mins)": (idx)*15,
                        "Weather Factor": weather_factor_value
                    })

            print(input_data)
            input_df = pd.DataFrame(input_data)

            # Encode categorical features
            for col in ["Traffic Level", "Weather Condition"]:
                input_df[col] = self.label_encoders[col].transform(input_df[col])

            # Standardize numerical features
            input_scaled = self.scaler.transform(input_df)

            # Predict Delivery Times
            predicted_delivery_times = self.model.predict(input_scaled)

            # Assign predicted times back to orders
            for order, pred_time in zip(assigned_orders_as_per_route, predicted_delivery_times):
                predicted_time = f'{int(pred_time/60)} hrs {int(pred_time%60)} mins'
                order.estimate_delivery_time = predicted_time  # Assign predicted time


            # Save route data in routes table
            route = Route(
                vehicle_id=vehicle.id,
                assigned_orders=str([o.id for o in assigned_orders_as_per_route]), 
                route=str(optimized_order_indexes),
                route_distance = distance[-1],
                full_route=str(full_route)
            )
            self.db.add(route)
            self.db.commit()

            # Update route_id in orders
            for order in assigned_orders_as_per_route:
                order.route_id = route.id 
            self.db.commit() 