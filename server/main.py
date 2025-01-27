from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
from models import Base, Order,Route, Vehicle
from order_manager import OrderManager
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import ast
# from enum import Enum as PyEnum


Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Allow specific origins
origins = [
    "*",  # React frontend
    "http://localhost:3000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all custom headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models to define the request/response schemas
class OrderCreate(BaseModel):
    name: str
    priority: int
    weight: float
    delivery_coordinates: str
    order_datetime: Optional[datetime] = None  # Make order_datetime optional as it will be auto-set
    status: Optional[str] = 'pending'
    delivery_distance: Optional[float] = None
    estimate_delivery_time: Optional[str] = None
    vehicle_id: Optional[int] = None
    route_id: Optional[int] = None

class OrderResponse(OrderCreate):
    id: int

    class Config:
        orm_mode = True



@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # If order_datetime is not provided, use the current timestamp
    if order.order_datetime is None:
        order.order_datetime = datetime.now()

    db_order = Order(
        name=order.name,
        priority = order.priority,
        weight=order.weight,
        delivery_coordinates=order.delivery_coordinates,
        order_datetime=order.order_datetime,
        status=order.status,
        estimate_delivery_time=order.estimate_delivery_time,
        vehicle_id=order.vehicle_id,
        route_id=order.route_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Assign orders & compute optimal routes
    manager = OrderManager(db)
    manager.assign_orders()

    return db_order

@app.get("/orders/", response_model=List[OrderResponse])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# Define request body model
class OrderRequest(BaseModel):
    order_ids: List[int]

@app.post("/orders_list/", response_model=List[OrderResponse])
def get_orders(order_request: OrderRequest, db: Session = Depends(get_db)):
    order_ids = order_request.order_ids

    # Fetch orders matching the given IDs
    orders = db.query(Order).filter(Order.id.in_(order_ids)).all()

    # Create a dictionary to maintain the order of requested IDs
    order_dict = {order.id: order for order in orders}

    # Check for missing order IDs
    missing_ids = [oid for oid in order_ids if oid not in order_dict]
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"Orders not found for IDs: {missing_ids}")

    # Return orders in the same order as requested
    return [order_dict[oid] for oid in order_ids]

class VehicleCreate(BaseModel):
    capacity: float


class VehicleResponse(VehicleCreate):
    id: int

    class Config:
        orm_mode = True


@app.post("/vehicles/", response_model=VehicleResponse)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):

    db_vehicle = Vehicle(
        capacity=vehicle.capacity,
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles/", response_model=List[VehicleResponse])
def get_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return vehicles

@app.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle



@app.get("/route/{vehicle_id}")
def get_route_by_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    # Fetch the order with the given vehicle_id
    order = db.query(Order).filter(Order.vehicle_id == vehicle_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="No orders found for this vehicle")
    
    # Fetch the associated route using order.route_id
    route = db.query(Route).filter(Route.id == order.route_id).first()
    
    if not route:
        raise HTTPException(status_code=404, detail="No route found for this vehicle's order")

    # Parse `full_route` into a proper list of lat/lng dictionaries
    try:
        parsed_full_route = eval(route.full_route)  # Assuming it's stored as a string representation of a list
        formatted_full_route = [{"lat": float(lat), "lng": float(lng)} for lat, lng in parsed_full_route]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing full_route: {str(e)}")
    
    return {
        "route_id": route.id,
        "assigned_orders": ast.literal_eval(route.assigned_orders),
        "route": route.route,
        "full_route": formatted_full_route,
        "vehicle_id": route.vehicle_id,
        "route_distance": route.route_distance
    }




@app.get("/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Get total number of orders
    total_orders = db.query(Order).count()

    # Get count of pending orders
    pending_orders = db.query(Order).filter(Order.status == "pending").count()

    # Get total number of vehicles
    total_vehicles = db.query(Vehicle).count()

    # Get count of vehicles with orders having status 'in-process'
    vehicles_with_in_process_orders = (
        db.query(Vehicle)
        .join(Order, Vehicle.id == Order.vehicle_id)
        .filter(Order.status == "in-process")
        .distinct()
        .count()
    )

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_vehicles": total_vehicles,
        "vehicles_with_in_process_orders": vehicles_with_in_process_orders
    }


