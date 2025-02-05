import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate  } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import KycDetails from './components/KycDetails';
import LoginPage from './components/Login';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/kyc/:kycId" element={<KycDetails /> } />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<LoginPage />} />
      </Routes>
    </Router>
  );
};

export default App;
