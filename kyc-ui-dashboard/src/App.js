import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import KycDetails from './components/KycDetails';
import LoginPage from './components/Login';

const App = () => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';  // Simulated authentication check
  return (
    <Router>
      <Routes>
        <Route path="/" element={isAuthenticated ? <Dashboard /> : <LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/kyc/:kycId" element={<KycDetails />} />
      </Routes>
    </Router>
  );
};

export default App;
