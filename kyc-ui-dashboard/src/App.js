import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import Dashboard from "./components/Dashboard";
import KycDetails from "./components/KycDetails";
import LoginPage from "./components/Login";
import LandingPage from "./components/LandingPage";
import DocumentUpload from "./components/DocumentUpload";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/kyc/:kycId" element={<KycDetails />} />
        <Route path="/landingPage" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin" element={<DocumentUpload />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  );
};

export default App;
