import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import L from 'leaflet';
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS

const OrderInputForm = () => {
  const [orderData, setOrderData] = useState({
    name: "",
    priority: 0,
    weight: 0,
    delivery_coordinates: "",
  });

  const mapRef = useRef(null);
  const markerRef = useRef(null);

  useEffect(() => {
    if (mapRef.current) {
      // Initialize the Leaflet map
      const map = L.map(mapRef.current).setView([19.076, 72.877], 12); // Default location: Mumbai

      // Add OpenStreetMap tile layer
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);

      // Add click event listener to the map
      map.on("click", (e) => {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        setOrderData((prev) => ({
          ...prev,
          delivery_coordinates: `${lat},${lng}`,
        }));

        // Remove previous marker if exists
        if (markerRef.current) {
          map.removeLayer(markerRef.current);
        }

        // Place new marker
        markerRef.current = L.marker([lat, lng]).addTo(map);
      });
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting Order:", orderData);

    try {
      const response = await axios.post("http://127.0.0.1:8000/orders", orderData);
      console.log("Order Created:", response.data);
      alert("Order successfully created!");
    } catch (error) {
      console.error("Error creating order:", error);
      alert("Failed to create order.");
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 bg-gray-900 text-white rounded-lg shadow-md mt-6">
      <h2 className="text-xl font-semibold mb-4 text-orange-400">Create New Order</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Order Name */}
        <div>
          <label className="block text-sm font-medium">Order Name</label>
          <input
            type="text"
            value={orderData.name}
            onChange={(e) => setOrderData({ ...orderData, name: e.target.value })}
            className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-white focus:ring-orange-500 focus:border-orange-500"
            required
          />
        </div>

        {/* Priority */}
      <div>
        <label className="block text-sm font-medium">Priority</label>
        <select
          value={orderData.priority}
          onChange={(e) => setOrderData({ ...orderData, priority: Number(e.target.value) })}
          className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-white focus:ring-orange-500 focus:border-orange-500"
          required
        >
          <option value={1}>High</option>
          <option value={2}>Moderate</option>
          <option value={3}>Low</option>
        </select>
      </div>

      {/* Weight */}
      <div>
        <label className="block text-sm font-medium">Weight (Kg)</label>
        <input
          type="number"
          value={orderData.weight}
          onChange={(e) => setOrderData({ ...orderData, weight: Math.max(0.01, parseFloat(e.target.value)) })}
          step="any" // Allows float input
          className="mt-1 block w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md shadow-sm text-white focus:ring-orange-500 focus:border-orange-500"
          required
        />
      </div>


        {/* Google Map for Pinning Location */}
        <div>
          <label className="block text-sm font-medium">Delivery Location</label>
          <div
            ref={mapRef}
            className="w-full"
            style={{ height: '300px', position: 'relative' }}
          ></div>
        </div>

        {/* Display Selected Coordinates */}
        <div>
          <label className="block text-sm font-medium">Selected Coordinates</label>
          <input
            type="text"
            value={orderData.delivery_coordinates}
            readOnly
            className="mt-1 block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md shadow-sm text-gray-300"
          />
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-orange-500 text-white py-2 px-4 rounded-md hover:bg-orange-600 transition"
        >
          Submit Order
        </button>
      </form>
    </div>
  );
};

export default OrderInputForm;
