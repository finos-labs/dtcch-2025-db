import React, { useState } from "react";
import { useParams } from "react-router-dom";

const KycDetails = () => {
  const { kycId } = useParams(); // Get the KYC ID from the URL
  const [selectedRequest, setSelectedRequest] = useState(null); // Store selected row data
  const [isModalOpen, setIsModalOpen] = useState(false); // Modal visibility state

  // KYC data with status tracking
  const kycData = {
    kycId: "KYC001",
    clientName: "Alice Smith",
    policy: "Policy A",
    triggerDate: "2024-02-01",
    status: "Verification",
    milestones: ["Initiated", "Documents Uploaded", "Verification", "Approved"],
    requirements: [
        { pid: 'PID001', requirement: 'Verify first name for Natural Person', action: 'first name', variable: 'name', status: 'Pending' },
        { pid: 'PID002', requirement: 'Verifiy Employee ID', action: 'Identification', variable: 'Emp ID', status: 'Completed', documents: 'Employer Provided Document' },
        { pid: 'PID003', requirement: 'Verifiy Citizenship', action: 'country', variable: 'citizenship', status: 'Completed', documents: 'Passport' },
      ],
  };

  // Find index of current milestone in the list
  const currentMilestoneIndex = kycData.milestones.indexOf(kycData.status);

  // Open modal and set selected request
  const handleRowClick = (request) => {
    setSelectedRequest(request);
    setIsModalOpen(true);
  };

  // Close modal
  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedRequest(null);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* KYC Details Header */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <h2 className="text-2xl font-semibold mb-4">KYC Details</h2>

        {/* Row 1 */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div><span className="font-semibold">KYC ID: </span>{kycData.kycId}</div>
          <div><span className="font-semibold">Client Name: </span>{kycData.clientName}</div>
          <div><span className="font-semibold">Policy: </span>{kycData.policy}</div>
          <div><span className="font-semibold">Trigger Date: </span>{kycData.triggerDate}</div>
        </div>

        {/* KYC Progress Bar */}
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">KYC Progress</h3>
          <div className="flex items-center justify-between">
            {kycData.milestones.map((step, index) => (
              <div key={index} className="flex flex-col items-center">
                <div
                  className={`w-8 h-8 flex items-center justify-center rounded-full text-white text-sm font-bold
                    ${index <= currentMilestoneIndex ? "bg-green-500" : "bg-gray-300"}`}
                >
                  {index + 1}
                </div>
                <span className="text-sm mt-1">{step}</span>
              </div>
            ))}
          </div>
          {/* Progress Line */}
          <div className="relative w-full h-1 bg-gray-300 mt-2">
            <div
              className="absolute h-1 bg-green-500"
              style={{ width: `${(currentMilestoneIndex / (kycData.milestones.length - 1)) * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Requirements</h3>
        <table className="w-full table-auto">
          <thead className="bg-gray-200">
            <tr>
              <th className="px-4 py-2 border">Pid</th>
              <th className="px-4 py-2 border">Requirement</th>
              <th className="px-4 py-2 border">Action</th>
              <th className="px-4 py-2 border">Variable</th>
              <th className="px-4 py-2 border">Status</th>
              <th className="px-4 py-2 border">Documents</th>
            </tr>
          </thead>
          <tbody>
            {kycData.requirements.map((request, index) => (
              <tr 
                key={index} 
                className="hover:bg-gray-100 cursor-pointer"
                onClick={() => handleRowClick(request)}
              >
                <td className="px-4 py-2 border">{request.pid}</td>
                <td className="px-4 py-2 border">{request.requirement}</td>
                <td className="px-4 py-2 border">{request.action}</td>
                <td className="px-4 py-2 border">{request.variable}</td>
                <td className="px-4 py-2 border">{request.status}</td>
                <td className="px-4 py-2 border">{request.documents}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Retrigger KYC Button */}
      <div className="mt-6 flex justify-left">
        <button 
          className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
        >
          Retrigger KYC
        </button>
      </div>

      {/* Modal Component */}
      {isModalOpen && selectedRequest && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-1/3">
            <h3 className="text-xl font-semibold mb-4">KYC Request Details</h3>
            <div className="space-y-2">
              <div><span className="font-semibold">Pid: </span>{selectedRequest.pid}</div>
              <div><span className="font-semibold">Requirement: </span>{selectedRequest.requirement}</div>
              <div><span className="font-semibold">Action: </span>{selectedRequest.action}</div>
              <div><span className="font-semibold">Variable: </span>{selectedRequest.variable}</div>
              <div><span className="font-semibold">Status: </span>{selectedRequest.status}</div>
              <div><span className="font-semibold">Documents: </span>{selectedRequest.documents}</div>
            </div>
            <div className="mt-4 flex justify-end">
              <button 
                onClick={closeModal} 
                className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KycDetails;
