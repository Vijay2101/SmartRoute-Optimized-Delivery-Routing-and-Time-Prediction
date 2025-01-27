import React, { useState, useEffect } from "react";
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import GoogleMapComponent from '../components/GoogleMapComponent';
import DashboardMetrics from '../components/DashboardMetrics';

const HomePage = () => {
  const warehouseLocation = { lat: 19.116458, lng: 72.902696 }; // Fixed warehouse location
  const deliveryLocation = { lat: 19.180458, lng: 72.849696 }; // Example destination
  const [routeData, setRouteData] = useState(null); // Store selected vehicle route data
  return (
    <>
      <Navbar />
      <div className="flex">
        {/* Sidebar on the Left */}
        <Sidebar setRouteData={setRouteData} />
        
        {/* Main Content (Map and Other Components) */}
        <div className="flex-1 max-w-7xl mx-auto pt-5 px-6">
          {/* Add Map and Other Sections Here */}

          <DashboardMetrics routeData={routeData} />
          {/* Add the Map component and pass origin and destination */}
          <GoogleMapComponent origin={warehouseLocation} destination={deliveryLocation} routeData={routeData} />
        </div>
      </div>
    </>
  );
};

export default HomePage;
