import React, { useEffect, useState } from "react";
import { UploadDocument, getPolicies } from "./api";
import { API_ENDPOINTS } from "./../config";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const DocumentUpload = () => {
  // Set the default document type to 'policy'
  const [documentType, setDocumentType] = useState("Policy");
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState(null);
  const [policyName, setPolicyName] = useState("");
  const [policyVersion, setPolicyVersion] = useState("");
  const [file, setFile] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        const [policiesData] = await Promise.all([getPolicies()]);
        setDocuments(policiesData);
      } catch (err) {
        setError("Error fetching documents");
        console.error(err);
      }
    };

    fetchDocuments();
  }, []);

  // Handle file input change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle form input change for document type, policy name, version
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    if (name === "documentType") {
      setDocumentType(value);
    } else if (name === "policyName") {
      setPolicyName(value);
    } else if (name === "policyVersion") {
      setPolicyVersion(value);
    }
  };

  // Handle form submission for file upload
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate input based on the selected document type
    if (!file || !documentType) {
      alert("Please fill out all required fields!");
      return;
    }

    if (documentType === "policy" && (!policyName || !policyVersion)) {
      alert("Please enter Policy Name and Policy Version.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("documentType", documentType);
    formData.append("policyName", policyName);
    formData.append("policyVersion", policyVersion);

    try {
      const response = await axios.post(
        `${API_ENDPOINTS.BASE_URL}/uploadDocument`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      // Add the uploaded file info to the state
      setDocuments([
        ...documents,
        {
          policy_file_path: response.data.policy_file_path,
          document_type: response.data.document_type,
          policy_name: response.data.policy_name,
          policy_version: response.data.policy_version,
        },
      ]);

      // Reset fields after successful upload
      setPolicyName("");
      setPolicyVersion("");
      setDocumentType("policy"); // Reset document type to 'policy'
      setFile(null); // Reset the file input
    } catch (error) {
      console.error("Error uploading document:", error);
    }
  };

  const viewDocument = async (filename) => {
    try {
      const response = await axios.get(
        `${API_ENDPOINTS.BASE_URL}/viewDocument`,
        {
          params: { filename },
          responseType: "blob", // Specify that the response is a file (for viewing or downloading)
        }
      );

      // Assuming the file is an image or PDF, you can open it in a new tab
      const fileURL = URL.createObjectURL(response.data);
      window.open(fileURL, "_blank"); // Open in a new tab
    } catch (err) {
      console.error("Error viewing document:", err);
      alert("Error viewing document.");
    }
  };

  const handleLogout = () => {
    // Add logic to logout the user, like clearing tokens or redirecting to login
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Header */}
      <header className="flex justify-between items-center rounded-lg mb-6">
        <h1 className="text-2xl font-bold block">Document Upload</h1>
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </header>

      {/* Upload Form */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-6">
        <form onSubmit={handleSubmit}>
          {/* Document Type Selection */}
          <div className="mb-4">
            <label className="block text-sm font-semibold">Document Type</label>
            <select
              name="documentType"
              value={documentType}
              onChange={handleInputChange}
              className="w-full p-2 border rounded-lg"
            >
              <option value="policy">Policy</option>
            </select>
          </div>

          {/* Additional Fields for Policy */}
          <div className="mb-4">
            <label className="block text-sm font-semibold">Policy Name</label>
            <input
              type="text"
              name="policyName"
              value={policyName}
              onChange={handleInputChange}
              className="w-full p-2 border rounded-lg"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold">
              Policy Version
            </label>
            <input
              type="text"
              name="policyVersion"
              value={policyVersion}
              onChange={handleInputChange}
              className="w-full p-2 border rounded-lg"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-semibold">Upload File</label>
            <input
              type="file"
              onChange={handleFileChange}
              className="w-full p-2 border rounded-lg"
              required
            />
          </div>

          <button
            type="submit"
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
          >
            Upload
          </button>
        </form>
      </div>

      {/* Display Uploaded Files */}
      {documents.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Uploaded Files</h3>
          <table className="w-full table-auto border-collapse shadow-lg">
            <thead>
              <tr className="bg-gray-200 text-gray-700">
                <th className="px-6 py-4 border-b text-left">Policy ID</th>
                <th className="px-6 py-4 border-b text-left">Document Type</th>
                <th className="px-6 py-4 border-b text-left">Policy Name</th>
                <th className="px-6 py-4 border-b text-left">Policy Version</th>
                <th className="px-6 py-4 border-b text-left">File</th>
                <th className="px-6 py-4 border-b text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((fileData, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 border-b">{fileData.policy_id}</td>
                  <td className="px-6 py-4 border-b">
                    {fileData.documentType || "Policy"}
                  </td>
                  <td className="px-6 py-4 border-b">
                    {fileData.policy_name || "N/A"}
                  </td>
                  <td className="px-6 py-4 border-b">
                    {fileData.policy_version || "N/A"}
                  </td>
                  <td className="px-6 py-4 border-b">
                    {fileData.policy_file_path}
                  </td>
                  <td className="px-6 py-4 border-b text-center">
                    <button
                      onClick={() => viewDocument(fileData.policy_file_path)}
                      className="text-blue-500 hover:text-blue-700 underline"
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
