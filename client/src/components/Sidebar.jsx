import { ChevronsLeft, ChevronsRight, Truck, Home, List } from "lucide-react";
import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo3.png";

const Sidebar = ({ setRouteData }) => {
  const [isOpen, setIsOpen] = useState(true);
  const [vehicles, setVehicles] = useState([]);
  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/vehicles");
        if (!response.ok) {
          throw new Error("Failed to fetch vehicles");
        }
        const data = await response.json();
        console.log(data)
        setVehicles(data);
      
      } catch (error) {
        console.error("Error fetching vehicles:", error);
      }
    };

    fetchVehicles();
  }, []);

  const fetchVehicleRoute = async (vehicleId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/route/${vehicleId}`);
      if (!response.ok) {
        throw new Error("Failed to fetch vehicle route");
      }
      const route = await response.json();
      console.log(route)
      setRouteData(route);
      console.log("assigned_orders:", route.assigned_orders);
      console.log("full_route:", route.full_route);
    } catch (error) {
      setRouteData(null);
      // console.error("Error fetching vehicle route:", error);
    }
  };

  return (
    <>
      {/* Sidebar Container */}
      <div className="relative flex">
        {/* Sidebar */}
        <div
          className={`h-screen bg-gray-900 text-white fixed top-16 left-0 z-40 transition-all duration-300 ${
            isOpen ? "w-64" : "w-0"
          } overflow-hidden`}
        >
          {isOpen && (
            <div>
              {/* Sidebar Header */}
              {/* <div className="flex justify-between items-center p-4 border-b border-gray-700">
                <Link to="/">
                  <img src={logo} alt="Logo" className="h-10 w-10" />
                </Link>
              </div> */}

              {/* Sidebar Menu */}
              <ul className="mt-6 space-y-4 px-4">

                {/* Dynamically Render Vehicles */}
                {vehicles.map((vehicle) => (
                  <li key={vehicle.id}>
                    <button
                      onClick={() => fetchVehicleRoute(vehicle.id)}
                      className="flex items-center p-3 hover:bg-gray-700 rounded-md w-full text-left"
                    >
                      <Truck size={20} className="mr-3" />
                      Vehicle {vehicle.id}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Sidebar Toggle Button (Always Visible) */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="fixed top-3 left-2 z-50 bg-gray-800 text-white p-2 rounded-md shadow-md"
        >
          {isOpen ? <ChevronsLeft size={24} /> : <ChevronsRight size={24} />}
        </button>
        
        {/* Main Content Area */}
        <div
          className={`transition-all duration-300 ${
            isOpen ? "ml-64" : "ml-0"
          } flex-1`}
        >
          {/* Here you can add the map or main content */}
        </div>
      </div>
    </>
  );
};

export default Sidebar;
