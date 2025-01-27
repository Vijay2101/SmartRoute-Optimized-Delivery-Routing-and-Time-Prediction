import React, { useState, useEffect } from "react";
import { GoogleMap, LoadScript, Polyline, Marker, InfoWindow } from "@react-google-maps/api";

const GoogleMapComponent = ({ routeData }) => {
  const [routePath, setRoutePath] = useState([
    { lat: 19.116458, lng: 72.902696 }, // Warehouse
  ]);

  const [orders, setOrders] = useState([]); // Store fetched order details
  const [selectedOrder, setSelectedOrder] = useState(null); // Track clicked marker

  useEffect(() => {
    if (routeData?.full_route) {
      setRoutePath(routeData.full_route);
    }

    if (routeData?.assigned_orders?.length) {
      fetchOrders(routeData.assigned_orders);
    }
    if (routeData== null){
      setOrders([]);
      setRoutePath([
        { lat: 19.116458, lng: 72.902696 }, // Warehouse
      ]);
    }
  }, [routeData]);

  // Fetch order details for given order IDs
  const fetchOrders = async (orderIds) => {
    try {
      const fetchedOrders = await Promise.all(
        orderIds.map(async (id) => {
          const response = await fetch(`http://127.0.0.1:8000/orders/${id}`);
          
          return response.json();
        })
      );
      setOrders(fetchedOrders);
    } catch (error) {
      console.error("Error fetching orders:", error);
    }
  };
  const warehouseCoordinates = { lat: 19.116458, lng: 72.902696 }; // Warehouse location
  return (
    <div>
      <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
        <GoogleMap
          mapContainerStyle={{ width: "100%", height: "70vh" }}
          center={routePath[0]}
          zoom={13}
        >
          {/* Route Path */}
          <Polyline
            path={routePath}
            options={{
              strokeColor: "#FF0000",
              strokeOpacity: 0.8,
              strokeWeight: 4,
            }}
          />

          {/* Markers for Orders */}
          {orders.map((order) => {
            const [lat, lng] = order.delivery_coordinates.split(",").map(Number);
            {console.log(lat,lng)}
            if (isNaN(lat) || isNaN(lng)) return null; // Skip invalid coords
            return (
              <Marker
                key={order.id}
                position={{ lat, lng }}
                label={{
                  text: order.name,
                  fontSize: "14px",
                  fontWeight: "bold",
                }}
                onClick={() => setSelectedOrder(order)} // Click to show InfoWindow
              />
            );
          })}

          {/* InfoWindow for selected order */}
          {selectedOrder && selectedOrder.delivery_coordinates &&(
            <InfoWindow
              position={{
                lat: parseFloat(selectedOrder.delivery_coordinates.split(",")[0]),
                lng: parseFloat(selectedOrder.delivery_coordinates.split(",")[1]),
              }}
              onCloseClick={() => setSelectedOrder(null)}
            >
              {/* {console.log("mila?:  :",selectedOrder)} */}
              <div style={{ color: "#000", padding: "5px", backgroundColor: "#fff" }}>
                <h3>Order: {selectedOrder.name}</h3>
                <p><strong>Priority:</strong> {selectedOrder.priority}</p>
                <p><strong>Weight:</strong> {selectedOrder.weight} kg</p>
                <p><strong>Status:</strong> {selectedOrder.status}</p>
                <p><strong>Distance:</strong> {selectedOrder.delivery_distance} Km</p>
                <p><strong>Estimated Delivery:</strong> {selectedOrder.estimate_delivery_time}</p>
              </div>
            </InfoWindow>
          )}


          {/* Warehouse Marker with InfoWindow always visible */}
          <Marker
            position={warehouseCoordinates}
            label={{
              text: "Warehouse",
              fontSize: "16px",
              fontWeight: "bold",
            }}
          />
          <InfoWindow
            position={warehouseCoordinates}
            onCloseClick={() => {}}
          >
            <div style={{ color: "#000", padding: "5px", backgroundColor: "#fff" }}>
              <h3 style={{ margin: "0", fontSize: "16px", fontWeight: "bold" }}>Warehouse</h3>
              <p><strong>Location:</strong> {`Lat: ${warehouseCoordinates.lat}, Lng: ${warehouseCoordinates.lng}`}</p>
            </div>
          </InfoWindow>
        </GoogleMap>
      </LoadScript>

      {/* Orders List */}
      <div className="p-6 bg-gray-800 rounded-lg shadow-md mt-6">
        <h1 className="text-3xl font-bold text-orange-400 mb-4">Assigned Orders</h1>
        {orders.length === 0 ? (
          <p className="text-gray-300">No orders assigned</p>
        ) : (
          <ul className="space-y-4">
            {console.log("ye hai orders",orders)}
            {orders.map((order) => (
              
              <li key={order.id} className="bg-gray-700 p-4 rounded-lg shadow-md">
                <p className="text-lg font-medium text-white">
                  <strong>Name:</strong> {order.name}
                </p>
                <p className="text-sm text-gray-300">
                  <strong>Priority:</strong> {order.priority}
                </p>
                <p className="text-sm text-gray-300">
                  <strong>Weight:</strong> {order.weight} kg
                </p>
                <p className="text-sm text-gray-300">
                  <strong>Status:</strong> {order.status}
                </p>
                <p className="text-sm text-gray-300">
                  <strong>Distance:</strong> {order.delivery_distance} Km
                </p>
                <p className="text-sm text-gray-300">
                  <strong>Estimated Delivery:</strong> {order.estimate_delivery_time}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>

    </div>
  );
};

export default GoogleMapComponent;
