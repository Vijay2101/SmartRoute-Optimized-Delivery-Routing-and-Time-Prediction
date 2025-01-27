import React from "react";
import VehicleInputForm from "../components/VehicleInputForm";
import Navbar from "../components/Navbar";

const VehiclePage = () => {
  const handleVehicleSubmit = (vehicleData) => {
    fetch("http://127.0.0.1:8000/vehicles/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(vehicleData),
    })
      .then((res) => res.json())
      .then((data) => console.log("Vehicle Added:", data))
      .catch((err) => console.error("Error:", err));
  };

  return (
    <>
      <Navbar />
      <div>
        <VehicleInputForm onSubmit={handleVehicleSubmit} />
      </div>
    </>
  );
};

export default VehiclePage;
