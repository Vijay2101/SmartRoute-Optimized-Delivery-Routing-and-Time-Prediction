// import { useState } from 'react'
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import GoogleMapPage from './pages/GoogleMapPage';
import HomePage from './pages/HomePage';
import OrderPage from './pages/OrderPage';
import VehiclesPage from './pages/VehiclesPage';

function App() {
  return (
    <Router>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/order" element={<OrderPage />} />
        <Route path="/vehicles" element={<VehiclesPage />} />
        {/* <Route path="/home" element={<HomePage />} /> */}
        {/* Protected routes */}

        {/* <Route element={<ProtectedRoute />}>
          <Route path="/home" element={<HomePage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/chats" element={<ChatListPage />} />
        </Route>
        
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/AuthRedirectPage" element={<AuthRedirectPage />} />
        <Route path="*" element={<LandingPage />} /> */}
        {/* Define other routes here */}
      </Routes>
    </Router>
  );
}

export default App;
