import React from "react";
import { Link } from "react-router-dom";

const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white p-10 rounded-lg shadow-lg text-center max-w-2xl">
        <h1 className="text-4xl font-bold text-blue-600">AI KYC Agent</h1>
        <p className="text-gray-700 mt-4">
          AI KYC Agent is an advanced solution designed to streamline and
          automate the Know Your Customer (KYC) process. It ensures compliance,
          enhances security, and accelerates verification through AI-driven
          automation.
        </p>

        <div className="mt-6 flex justify-center space-x-4">
          <Link to="/dashboard">
            <button className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
              Go to Dashboard
            </button>
          </Link>

          <Link to="/admin">
            <button className="bg-green-500 text-white px-6 py-2 rounded-lg hover:bg-green-600">
              Admin Upload
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;
