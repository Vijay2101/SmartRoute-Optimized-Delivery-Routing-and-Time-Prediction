from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base

# Define the Order model
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    delivery_coordinates = Column(String, nullable=False)
    order_datetime = Column(DateTime, nullable=False)
    status = Column(String, default='pending')
    delivery_distance = Column(Float, nullable=True) 
    estimate_delivery_time = Column(String, nullable=True)
    
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=True)
    
    # 🔹 Add comparison method for heapq
    def __lt__(self, other):
        return self.priority < other.priority 
    
    def __repr__(self):
        return f"Order(id={self.id}, name={self.name}, weight={self.weight}, status={self.status})"

# Define the Vehicle model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    capacity = Column(Float, nullable=False)
    # current_capacity = Column(Float, nullable=True)
    # available = Column(Boolean, default=True)

    assigned_orders = relationship("Order", backref="vehicle")
    assigned_routes = relationship("Route", backref="vehicle")

    def __repr__(self):
        return f"Vehicle(id={self.id}, capacity={self.capacity}, available={self.available})"

# Define the Route model
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    assigned_orders = Column(String, nullable=False)
    route = Column(String, nullable=False)  # JSON or comma-separated list of warehouse & delivery coordinates
    full_route = Column(String, nullable=False)  # JSON or comma-separated list of all coordinates
    route_distance = Column(Float, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    
    def __repr__(self):
        return f"Route(id={self.id}, vehicle_id={self.vehicle_id})"
