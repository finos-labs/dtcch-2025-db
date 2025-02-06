import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getKycDetail, getActionsList } from "./api";

const KycDetails = () => {
  const { kycId } = useParams(); // Get the KYC ID from the URL
  const navigate = useNavigate();

  const [error, setError] = useState(null);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [kycDetail, setKycDetail] = useState(null);
  const [actionsList, setActionsList] = useState([]);
  const [loading, setLoading] = useState(true); // Loading state
  const [sortOrder, setSortOrder] = useState("asc"); // "asc" or "desc"

  const capitalizeFirstLetter = (str) => {
    return str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : "";
  };

  useEffect(() => {
    const fetchKycDetails = async () => {
      const token = localStorage.getItem("token");

      if (!token) {
        setError("Session expired. Please log in again.");
        navigate("/login");
        return;
      }

      try {
        // Fetch both KYC details and actions list simultaneously
        // Fetch both KYC details and actions list simultaneously
        const [kycDetailResponse, actionsListResponse] = await Promise.all([
          getKycDetail(kycId),
          getActionsList(kycId),
        ]);

        console.log("KYC Detail Response:", kycDetailResponse);
        console.log("Actions List Response:", actionsListResponse);

        // Ensure data is correctly extracted
        setKycDetail(kycDetailResponse);
        const sortedData = actionsListResponse.sort(
          (a, b) => a.action_id - b.action_id
        ); // Sort ascending initially
        setActionsList(sortedData || []);
      } catch (err) {
        console.error("Error fetching KYC details:", err);
        setError("Failed to fetch data. Please try again.");
        localStorage.removeItem("token");
        navigate("/login");
      } finally {
        setLoading(false); // Stop loading
      }
    };

    if (kycId) {
      fetchKycDetails();
    }
  }, [kycId, navigate]);

  // Sorting function for ACTION ID
  const handleSortById = () => {
    const sortedData = [...actionsList].sort((a, b) =>
      sortOrder === "asc"
        ? b.action_id - a.action_id
        : a.action_id - b.action_id
    );

    setActionsList(sortedData);
    setSortOrder(sortOrder === "asc" ? "desc" : "asc"); // Toggle sort order
  };

  // Prevent rendering before data is loaded
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p className="text-lg font-semibold">Loading...</p>
      </div>
    );
  }

  const statuses = ["New", "Verification", "Completed"];
  const currentMilestoneIndex = statuses.indexOf(
    capitalizeFirstLetter("Verification") || ""
  );

  // Open modal
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

        {/* KYC Info */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          {/* KYC ID */}
          <div className="flex items-center space-x-3">
            <span className="text-gray-500 font-semibold">🔍 KYC ID:</span>
            <span className="text-gray-700">{kycDetail?.kyc_id || "N/A"}</span>
          </div>
          {/* Client Name */}
          <div className="flex items-center space-x-3">
            <span className="text-gray-500 font-semibold">👤 Client Name:</span>
            <span className="text-gray-700">
              {kycDetail?.client_name || "N/A"}
            </span>
          </div>

          {/* Policy Name */}
          <div className="flex items-center space-x-3">
            <span className="text-gray-500 font-semibold">📜 Policy:</span>
            <span className="text-gray-700">
              {kycDetail?.policy_name || "N/A"}
            </span>
          </div>

          {/* Trigger Date */}
          <div className="flex items-center space-x-3">
            <span className="text-gray-500 font-semibold">
              📅 Trigger Date:
            </span>
            <span className="text-gray-700">
              {kycDetail?.trigger_date || "N/A"}
            </span>
          </div>

          {/* Status */}
          <div className="flex items-center space-x-3 col-span-1 md:col-span-2">
            <span className="text-gray-500 font-semibold">🚦 Status:</span>
            <span
              className={`px-3 py-1 rounded-lg text-white text-sm font-semibold
          ${
            kycDetail?.status === "Completed"
              ? "bg-green-500"
              : kycDetail?.status === "Verification"
              ? "bg-yellow-500"
              : "bg-red-500"
          }
        `}
            >
              {kycDetail?.status || "N/A"}
            </span>
          </div>
        </div>

        {/* KYC Progress Bar */}
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-4 text-center">
            KYC Progress
          </h3>

          {/* Progress Bar Wrapper */}
          <div className="relative flex items-center w-full">
            {/* Full Progress Line (Gray Background) */}
            <div className="absolute left-0 right-0 h-1 bg-gray-300"></div>

            {/* Highlighted Progress Line (Fills Until Selected Milestone) */}
            <div
              className="absolute left-0 h-1 bg-green-500 transition-all duration-300"
              style={{
                width: `${
                  (currentMilestoneIndex / (statuses.length - 1)) * 100
                }%`,
              }}
            ></div>

            {/* Milestone Steps (Placed on the Progress Line) */}
            {statuses.map((step, index) => (
              <div
                key={index}
                className="relative flex flex-col items-center w-full"
              >
                {/* Milestone Circle (Positioned on Progress Bar) */}
                <div
                  className={`w-10 h-10 flex items-center justify-center rounded-full text-white text-sm font-bold transition-all duration-300
            ${index <= currentMilestoneIndex ? "bg-green-500" : "bg-gray-300"}`}
                >
                  {index + 1}
                </div>
                {/* Step Label */}
                <span className="text-sm mt-2 text-center">{step}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Actions</h3>
        <table className="w-full table-auto">
          <thead className="bg-gray-200">
            <tr>
              <th
                className="px-4 py-2 border cursor-pointer"
                onClick={handleSortById}
              >
                Action ID {sortOrder === "asc" ? "🔼" : "🔽"}
              </th>
              <th className="px-4 py-2 border">Data Point</th>
              <th className="px-4 py-2 border">Status</th>
              <th className="px-4 py-2 border">Action Description</th>
            </tr>
          </thead>
          <tbody>
            {actionsList?.map((action, index) => (
              <tr
                key={index}
                className="hover:bg-gray-100 cursor-pointer"
                onClick={() => handleRowClick(action)}
              >
                <td className="px-4 py-2 border">{action.action_id}</td>
                <td className="px-4 py-2 border">{action.data_point}</td>
                <td className="px-4 py-2 border">{action.status}</td>
                <td className="px-4 py-2 border">
                  {action.action_description}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Retrigger KYC Button */}
      <div className="mt-6 flex justify-left">
        <button className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600">
          Retrigger KYC
        </button>
      </div>

      {/* Modal Component */}
      {isModalOpen && selectedRequest && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-[80%] max-w-3xl">
            <h3 className="text-xl font-semibold mb-4 text-center">
              KYC Request Details
            </h3>

            {/* Table */}
            <table className="w-full border-collapse border border-gray-300">
              <tbody>
                {[
                  ["KYC ID", selectedRequest?.kyc_id],
                  ["Action Description", selectedRequest?.action_description],
                  ["Business Type", selectedRequest?.business_type],
                  [
                    "Client Evidence Source",
                    selectedRequest?.client_evidence_source,
                  ],
                  ["Data Point", selectedRequest?.data_point],
                  ["Due Diligence Level", selectedRequest?.due_diligence_level],
                  ["Entity Type", selectedRequest?.entity_type],
                  [
                    "External Evidence Source",
                    selectedRequest?.external_evidence_source?.join(", "),
                  ],
                  [
                    "Internal Evidence Source",
                    selectedRequest?.internal_evidence_source?.join(", "),
                  ],
                  [
                    "Latest Action Activity",
                    selectedRequest?.latest_action_activity,
                  ],
                  ["Policy Quote", selectedRequest?.policy_quote],
                  ["Role", selectedRequest?.role],
                ].map(([label, value], index) => (
                  <tr key={index} className="border border-gray-300">
                    <td className="px-4 py-2 font-semibold bg-gray-200">
                      {label}
                    </td>
                    <td className="px-4 py-2">{value || "N/A"}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* Close Button */}
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
