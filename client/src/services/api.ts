import axios from 'axios';

// Create an instance of Axios with a base URL
const apiClient = axios.create({
  baseURL: 'https://jmelzacki.com/api', // Replace with your backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

export const register = async (credentials: { email: string; username: string; password: string }) => {
  return apiClient.post("/register", credentials);
};

export const userData = async (token: string): Promise<{ username: string; email: string; }> => {
    const response = await apiClient.get('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
};

export default apiClient;