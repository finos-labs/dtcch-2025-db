import React, { useEffect, useState } from "react";
import {
  getUserInfo,
  getKycRequests,
  getClients,
  getPolicies,
  triggerKyc,
} from "./api";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [kycRequests, setKycRequests] = useState([]);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState("");
  const [selectedPolicy, setSelectedPolicy] = useState("");
  const [sortOrder, setSortOrder] = useState("asc"); // "asc" or "desc"

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

  const handleCloseModal = () => setIsModalOpen(false);

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
      alert("New Kyc is triggrered !");
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

  const handleSortById = () => {
    const sortedData = [...kycRequests].sort((a, b) =>
      sortOrder === "asc" ? b.kyc_id - a.kyc_id : a.kyc_id - b.kyc_id
    );

    setKycRequests(sortedData);
    setSortOrder(sortOrder === "asc" ? "desc" : "asc"); // Toggle sort order
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* User Info & Logout */}
      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between mb-6">
        {user ? (
          <div className="flex items-center gap-4">
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
            </div>
          </div>
        ) : (
          <p className="text-gray-500">Loading user data...</p>
        )}

        <button
          onClick={handleLogout}
          className="text-red-500 hover:text-red-600 font-semibold px-4 py-2 rounded transition"
        >
          Logout
        </button>
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
                onClick={handleSortById}
              >
                KYC ID {sortOrder === "asc" ? "🔼" : "🔽"}
              </th>
              <th className="border p-3">Client Name</th>
              <th className="border p-3">Policy</th>
              <th className="border p-3">Trigger Date</th>
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
                  <td className="border p-3">{request.trigger_date}</td>
                  <td
                    className={`border p-3 font-semibold ${
                      request.status === "Approved"
                        ? "text-green-500"
                        : request.status === "Pending"
                        ? "text-yellow-500"
                        : "text-red-500"
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
