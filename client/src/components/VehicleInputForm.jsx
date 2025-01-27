import React, { useState } from "react";
import axios from "axios";

const VehicleInputForm = () => {
  const [vehicleData, setVehicleData] = useState({
    capacity: 0,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting Vehicle:", vehicleData);

    try {
      const response = await axios.post("http://127.0.0.1:8000/vehicles", vehicleData);
      console.log("Vehicle Added:", response.data);
      alert("Vehicle successfully added!");
    } catch (error) {
      console.error("Error adding vehicle:", error);
      alert("Failed to add vehicle.");
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-gray-900 text-white rounded-lg shadow-md mt-6">
      <h2 className="text-xl font-semibold mb-4 text-orange-400">Add New Vehicle</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Vehicle Capacity */}
        <div>
          <label className="block text-sm font-medium">Vehicle Capacity</label>
          <input
            type="number"
            value={vehicleData.capacity}
            onChange={(e) => setVehicleData({ ...vehicleData, capacity: Number(e.target.value) })}
            className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-white focus:ring-orange-500 focus:border-orange-500"
            required
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-orange-500 text-white py-2 px-4 rounded-md hover:bg-orange-600 transition"
        >
          Submit Vehicle
        </button>
      </form>
    </div>
  );
};

export default VehicleInputForm;
