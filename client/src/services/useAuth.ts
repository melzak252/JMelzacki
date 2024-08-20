import { ref } from 'vue';
import { getTokenCookie, removeTokenCookie } from '../services/cookies';
import { userData } from '../services/api';

const isAuthenticated = ref<boolean>(!!getTokenCookie());
const user = ref<{ username: string; email: string } | null>(null);

export function useAuth() {
  const fetchUserData = async () => {
    const token = getTokenCookie();
    if (!token) return;
    console.log(token)

    try {
      let apiUser = await userData(token)
      user.value = apiUser; // Set the username from the response
    } catch (error) {
      console.error('Failed to fetch user data:', error);
      logout(); // If fetching user data fails, consider logging the user out
    }
  };

  const login = (token: string) => {
    isAuthenticated.value = true;
    fetchUserData()
  };

  const logout = () => {
    removeTokenCookie();
    isAuthenticated.value = false;
    user.value = null;
  };

  return {
    isAuthenticated,
    user,
    fetchUserData,
    login,
    logout,
  };
}