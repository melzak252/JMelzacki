import { ref } from 'vue';
import axios from 'axios';
import config from '../config.json';

const isAuthenticated = ref<boolean>(false);
const user = ref<{ username: string; email: string } | null>(null);

export function useAuth() {
  const fetchUserData = async (): Promise<boolean> => {
    try {
      const response = await axios.get(`${config.apiUrl}/users/me`, {
        withCredentials: true
      });
      let apiUser = response.data;
      user.value = apiUser; // Set the username from the response'
      return !!apiUser;
    } catch (error) {
      return false;
    }
  };

  const login = async () => {
    isAuthenticated.value = await fetchUserData();

  };

  const logout = async () => {
    isAuthenticated.value = false;
    user.value = null;

    await axios.post(`${config.apiUrl}/logout`, {},
      {
        withCredentials: true
      });
  };

  return {
    isAuthenticated,
    user,
    fetchUserData,
    login,
    logout,
  };
}