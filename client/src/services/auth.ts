
import axios from 'axios';

const apiClient = axios.create({
  baseURL: "http://localhost:8080", // Replace with your backend URL
  headers: {
    "Content-Type": "application/x-www-form-urlencoded", // Use form-encoded data
  },
});

export const login = async (credentials: { username: string; password: string }) => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  return apiClient.post("/login", formData);
};
