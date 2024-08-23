import { ref } from 'vue';
import axios from 'axios';

const isAuthenticated = ref<boolean>(false);
const user = ref<{ username: string; email: string } | null>(null);

export function useAuth() {
  const fetchUserData = async (): Promise<boolean> => {
    try {
      const response = await axios.get('https://jmelzacki.com/api/users/me', {
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