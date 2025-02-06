import axios from "axios";
import { API_ENDPOINTS } from "./../config";

const api = axios.create({
  baseURL: API_ENDPOINTS.BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// Add Authorization token to requests
api.interceptors.request.use((config) => {  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const loginUser = (credentials) => api.post("/login", credentials);
export const getUserInfo = async () => {
  const token = localStorage.getItem("token");
  return axios.get(`${API_ENDPOINTS.BASE_URL}/user`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const getKycRequests = async () => {
  const token = localStorage.getItem("token");
  
  return axios.get(`${API_ENDPOINTS.BASE_URL}/getKycList`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const getClients = async () => {
  const token = localStorage.getItem("token");
  
  const response = await fetch(`${API_ENDPOINTS.BASE_URL}/clients`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  console.log(response)
  if (!response.ok) throw new Error("Failed to fetch clients");
  return response.json();
};

export const getPolicies = async () => {
  const token = localStorage.getItem("token");
  
  const response = await fetch(`${API_ENDPOINTS.BASE_URL}/policies`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error("Failed to fetch policies");
  return response.json();
};


export const triggerKyc = async (requestData) => {
  const token = localStorage.getItem("token");

  try {
    console.log('trigger kyc for ', requestData)
     const response = await axios.post(
      `${API_ENDPOINTS.BASE_URL}/triggerKyc`,
      requestData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error triggering KYC:", error.response?.data || error.message);
    throw error.response?.data || error.message;
  }
};

export const getKycDetail = async (kycId) => {
  const token = localStorage.getItem("token");
  
  const response = await fetch(`${API_ENDPOINTS.BASE_URL}/kyc/${kycId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error("Failed to fetch kycDetails");
  return response.json();
};

export const getActionsList = async (kycId) => {
  const token = localStorage.getItem("token");
  
  const response = await fetch(`${API_ENDPOINTS.BASE_URL}/actionsList/${kycId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!response.ok) throw new Error("Failed to fetch getActionsList");
  return response.json();
};
