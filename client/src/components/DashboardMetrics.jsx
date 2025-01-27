import { useEffect, useState } from "react";

const DashboardMetrics = ({ routeData }) => {
  const [stats, setStats] = useState({
    total_orders: 0,
    pending_orders: 0,
    total_vehicles: 0,
    vehicles_with_in_process_orders: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/dashboard-stats");
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
      }
    };
    fetchStats();
  }, []);
  // Assuming fuel price 103rs and a delivery vehicle can travel 17.2km with 1L fuel
  const cost_perKM =103/17.2
  const costEfficiency = routeData ? (routeData.route_distance * cost_perKM).toFixed(2) : "N/A"; // Assuming cost = 0.5 per km

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 p-4">
      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Total Orders</h2>
        <p className="text-white text-2xl">{stats.total_orders}</p>
      </div>

      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Pending Orders</h2>
        <p className="text-white text-2xl">{stats.pending_orders}</p>
      </div>

      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Total Vehicles</h2>
        <p className="text-white text-2xl">{stats.total_vehicles}</p>
      </div>

      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Active Vehicles</h2>
        <p className="text-white text-2xl">{stats.vehicles_with_in_process_orders}</p>
      </div>

      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Route Distance</h2>
        <p className="text-white text-2xl">{routeData?.route_distance ?? "N/A"} Km</p>
      </div>

      <div className="p-4 bg-gray-800 rounded-lg shadow-md text-center">
        <h2 className="text-xl font-bold text-orange-400">Cost Efficiency</h2>
        <p className="text-white text-2xl">₹{costEfficiency}</p>
      </div>
    </div>
  );
};

export default DashboardMetrics;
