// const API_BASE_URL = "http://localhost:5000";
const API_BASE_URL = "http://dtcch-2025-db.sibnick.men:5000/"; // Change this to your actual API URL

export const API_ENDPOINTS = {
  BASE_URL: `${API_BASE_URL}/`,    
  GET_DATA: `${API_BASE_URL}/data`,
  POST_DATA: `${API_BASE_URL}/submit`,
  AUTH_LOGIN: `${API_BASE_URL}/auth/login`,
  AUTH_REGISTER: `${API_BASE_URL}/auth/register`,
  USER_DATA: `${API_BASE_URL}/user`,
};