import React, { useEffect, useState } from "react";
import {
  getUserInfo,
  getKycRequests,
  getClients,
  getPolicies,
  triggerKyc,
} from "./api";
import { useNavigate } from "react-router-dom";
import appImage from "./../images/favicon.webp"; // Import the image

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [kycRequests, setKycRequests] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState("");
  const [selectedPolicy, setSelectedPolicy] = useState("");
  const [sortOrder, setSortOrder] = useState({
    kyc_id: "asc", // Default sort order for KYC ID
    client_name: "asc", // Default sort order for Client Name
    policy_name: "asc", // Default sort order for Policy
    trigger_date: "asc", // Default sort order for Trigger Date
  });

  const [clients, setClients] = useState([]);
  const [policies, setPolicies] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("Session expired. Please log in again.");
        navigate("/");
        return;
      }

      try {
        const [userResponse, kycResponse] = await Promise.all([
          getUserInfo(),
          getKycRequests(),
        ]);

        setUser(userResponse.data);
        const sortedData = kycResponse.data.sort((a, b) => a.kyc_id - b.kyc_id); // Sort ascending initially
        console.log(sortedData);
        setKycRequests(sortedData || []);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Session expired. Please log in again.");
        localStorage.removeItem("token");
        navigate("/login");
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleRowClick = (kycId) => {
    navigate(`/kyc/${kycId}`);
  };

  const handleOpenModal = async () => {
    try {
      const [clientsData, policiesData] = await Promise.all([
        getClients(),
        getPolicies(),
      ]);

      setClients(clientsData);
      setPolicies(policiesData);

      setIsModalOpen(true); // Open modal after fetching data
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedClient("");
    setSelectedPolicy("");
  };

  const handleSubmit = async () => {
    if (!selectedClient || !selectedPolicy) {
      alert("Please select a client and policy.");
      return;
    }

    try {
      const requestData = {
        client_id: selectedClient, // Ensure this holds the client's ID
        policy_id: selectedPolicy, // Ensure this holds the policy's ID
      };

      const response = await triggerKyc(requestData);
      alert("New KYC triggered!");
      // Add the new KYC request to the state

      const kycResponse = await getKycRequests();
      setKycRequests(kycResponse.data);

      handleCloseModal(); // Close modal
    } catch (error) {
      alert(error.error || "Failed to trigger KYC. Please try again.");
    }
  };

  const filteredRequests = kycRequests.filter((request) =>
    Object.values(request).some((value) =>
      value.toString().toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  const handleSort = (column) => {
    const newSortOrder = sortOrder[column] === "asc" ? "desc" : "asc";
    setSortOrder({
      ...sortOrder,
      [column]: newSortOrder,
    });

    const sortedData = [...kycRequests].sort((a, b) => {
      if (column === "kyc_id") {
        return newSortOrder === "asc"
          ? a.kyc_id - b.kyc_id
          : b.kyc_id - a.kyc_id;
      }
      if (column === "client_name") {
        return newSortOrder === "asc"
          ? a.client_name.localeCompare(b.client_name)
          : b.client_name.localeCompare(a.client_name);
      }
      if (column === "policy_name") {
        return newSortOrder === "asc"
          ? a.policy_name.localeCompare(b.policy_name)
          : b.policy_name.localeCompare(a.policy_name);
      }
      if (column === "trigger_date") {
        return newSortOrder === "asc"
          ? new Date(a.trigger_date) - new Date(b.trigger_date)
          : new Date(b.trigger_date) - new Date(a.trigger_date);
      }
      return 0;
    });

    setKycRequests(sortedData);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* User Info & Logout */}
      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between mb-6">
        {/* Left Side: AI KYC Agent Text */}
        <div className="flex items-center">
          <img src={appImage} alt="AI KYC" className="mr-4 w-20 h-20" />
          <div className="flex-1">
            <p className="font-bold text-5xl text-gray-800">AI KYC Agent</p>
          </div>
        </div>

        {/* Right Side: User Details and Logout Button */}
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <img
                src={user.avatar || "https://i.pravatar.cc/100"}
                alt="Avatar"
                className="w-16 h-16 rounded-full border-2 border-gray-300 shadow-sm"
              />
              <div>
                <h2 className="text-xl font-semibold text-gray-800">
                  {user.name}
                </h2>
                <p className="text-gray-500">{user.email}</p>
                <p className="text-gray-600 font-medium">{user.department}</p>

                {/* Logout Button */}
                <button
                  onClick={handleLogout}
                  className="text-blue-500 hover:text-red-600 font-semibold px-4 py-2 rounded transition"
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <p className="text-gray-500">Loading user data...</p>
          )}
        </div>
      </div>

      {/* Search Input */}
      <div className="bg-white p-4 rounded-lg shadow-md mb-4">
        <input
          type="text"
          placeholder="Search by KYC ID, Client Name, Policy, or Status..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full p-2 border rounded-lg"
        />
      </div>

      {/* KYC Requests Table */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold mb-4">KYC Requests</h2>
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-200">
              <th
                className="px-4 py-2 border cursor-pointer"
                onClick={() => handleSort("kyc_id")}
              >
                KYC ID {sortOrder.kyc_id === "asc" ? "↑" : "↓"}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer"
                onClick={() => handleSort("client_name")}
              >
                Client Name {sortOrder.client_name === "asc" ? "↑" : "↓"}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer"
                onClick={() => handleSort("policy_name")}
              >
                Policy {sortOrder.policy_name === "asc" ? "↑" : "↓"}
              </th>
              <th
                className="px-4 py-2 border cursor-pointer"
                onClick={() => handleSort("trigger_date")}
              >
                Trigger Date {sortOrder.trigger_date === "asc" ? "↑" : "↓"}
              </th>
              <th className="border p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredRequests.length > 0 ? (
              filteredRequests.map((request, index) => (
                <tr
                  key={index}
                  className="text-center bg-white hover:bg-gray-50 cursor-pointer"
                  onClick={() => handleRowClick(request.kyc_id)}
                >
                  <td className="border p-3">{request.kyc_id}</td>
                  <td className="border p-3">{request.client_name}</td>
                  <td className="border p-3">{request.policy_name}</td>
                  <td className="border p-3">
                    {new Date(request.trigger_date).toLocaleDateString(
                      "en-US",
                      {
                        weekday: "long", // e.g., 'Monday'
                        year: "numeric", // e.g., '2025'
                        month: "long", // e.g., 'February'
                        day: "numeric", // e.g., '6'
                      }
                    )}
                  </td>
                  <td
                    className={`border p-3 font-semibold ${
                      request.status === "COMPLETED"
                        ? "text-green-500"
                        : request.status === "IN PROGRESS"
                        ? "text-yellow-500"
                        : "text-blue-500"
                    }`}
                  >
                    {request.status}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-gray-500 p-4">
                  No matching results found.
                </td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Trigger KYC Button */}
        <button
          onClick={handleOpenModal}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Trigger KYC
        </button>

        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 flex justify-center items-center bg-gray-500 bg-opacity-50">
            <div className="bg-white p-6 rounded-lg shadow-lg w-[80%] max-w-3xl">
              <h2 className="text-xl font-semibold mb-4">
                Select Client and Policy
              </h2>
              <div className="mb-4">
                <label className="block text-gray-700">Client</label>
                {/* Clients Dropdown */}
                <select
                  value={selectedClient}
                  onChange={(e) =>
                    setSelectedClient(
                      e.target.options[e.target.selectedIndex].id
                    )
                  }
                  className="w-full p-2 border rounded-lg"
                >
                  <option value="">Select Client</option>
                  {clients.map((client, index) => (
                    <option
                      key={client.client_id}
                      value={client.client_id}
                      id={client.client_id}
                    >
                      {client.client_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-gray-700">Policy</label>
                {/* Policies Dropdown */}
                <select
                  value={selectedPolicy}
                  onChange={(e) =>
                    setSelectedPolicy(
                      e.target.options[e.target.selectedIndex].id
                    )
                  }
                  className="w-full p-2 border rounded-lg"
                >
                  <option value="">Select Policy</option>
                  {policies.map((policy, index) => (
                    <option
                      key={policy.policy_id}
                      value={policy.policy_id}
                      id={policy.policy_id}
                    >
                      {policy.policy_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex justify-between">
                <button
                  onClick={handleCloseModal}
                  className="px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
                >
                  Cancel
                </button>
                <button
                  onClick={handleSubmit}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  Submit
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
