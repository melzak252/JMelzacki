import { ref } from 'vue';
import { userData } from '../services/api';
import axios from 'axios';

const isAuthenticated = ref<boolean>(false);
const user = ref<{ username: string; email: string } | null>(null);

export function useAuth() {
  const fetchUserData = async (): Promise<boolean> => {
    try {
      let apiUser = await userData()
      user.value = apiUser; // Set the username from the response
      return !!apiUser;
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      return false;
    }
  };

  const login = async () => {
    isAuthenticated.value = await fetchUserData();

  };

  const logout = async () => {
    isAuthenticated.value = false;
    user.value = null;

    await axios.post('https://jmelzacki.com/api/logout', {},
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