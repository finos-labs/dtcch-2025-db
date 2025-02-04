import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const user = {
  name: 'John Doe',
  email: 'john.doe@example.com',
  department: 'Compliance',
  avatar: 'https://i.pravatar.cc/100',
};

const Dashboard = () => {
  const navigate = useNavigate();  // Hook to navigate to other pages
  const [kycRequests, setKycRequests] = useState([
    { id: 'KYC001', clientName: 'Alice Smith', policy: 'Policy A', triggerDate: '2024-02-01', status: 'Pending' },
    { id: 'KYC002', clientName: 'Bob Johnson', policy: 'Policy B', triggerDate: '2024-02-02', status: 'Approved' },
    { id: 'KYC003', clientName: 'Charlie Brown', policy: 'Policy C', triggerDate: '2024-02-03', status: 'Rejected' },
  ]);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredRequests = kycRequests.filter((request) =>
    Object.values(request).some((value) =>
      value.toString().toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  const handleRowClick = (kycId) => {
    // Navigate to the details page with the selected KYC ID
    navigate(`/kyc/${kycId}`);
  };

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedClient, setSelectedClient] = useState("");
  const [selectedPolicy, setSelectedPolicy] = useState("");

  const clients = [
    "Alice Smith",
    "Bob Johnson",
    "Charlie Brown",
  ];

  const policies = [
    "Policy A",
    "Policy B",
    "Policy C",
  ];


  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleSubmit = () => {
    // Add logic to trigger KYC request based on selectedClient and selectedPolicy
    console.log("Selected Client:", selectedClient);
    console.log("Selected Policy:", selectedPolicy);
    handleCloseModal(); // Close the modal after submission
  };


  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* User Info & Logout */}
      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <img src={user.avatar} alt="Avatar" className="w-16 h-16 rounded-full" />
          <div>
            <h2 className="text-xl font-semibold">{user.name}</h2>
            <p className="text-gray-500">{user.email}</p>
            <p className="text-gray-600 font-medium">{user.department}</p>
          </div>
        </div>
        <button className="text-red-500 hover:underline">Logout</button>
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
              <th className="border p-3">KYC ID</th>
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
                  onClick={() => handleRowClick(request.id)} // Navigate to the details page on click
                >
                  <td className="border p-3">{request.id}</td>
                  <td className="border p-3">{request.clientName}</td>
                  <td className="border p-3">{request.policy}</td>
                  <td className="border p-3">{request.triggerDate}</td>
                  <td
                    className={`border p-3 font-semibold ${
                      request.status === 'Approved'
                        ? 'text-green-500'
                        : request.status === 'Pending'
                        ? 'text-yellow-500'
                        : 'text-red-500'
                    }`}
                  >
                    {request.status}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-gray-500 p-4">No matching results found.</td>
              </tr>
            )}
          </tbody>
        </table>

          {/* Trigger KYC Button */}
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
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4">Select Client and Policy</h2>
            <div className="mb-4">
              <label className="block text-gray-700">Client</label>
              <select
                value={selectedClient}
                onChange={(e) => setSelectedClient(e.target.value)}
                className="w-full p-2 border rounded-lg"
              >
                <option value="">Select Client</option>
                {clients.map((client, index) => (
                  <option key={index} value={client}>
                    {client}
                  </option>
                ))}
              </select>
            </div>
            <div className="mb-4">
              <label className="block text-gray-700">Policy</label>
              <select
                value={selectedPolicy}
                onChange={(e) => setSelectedPolicy(e.target.value)}
                className="w-full p-2 border rounded-lg"
              >
                <option value="">Select Policy</option>
                {policies.map((policy, index) => (
                  <option key={index} value={policy}>
                    {policy}
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
