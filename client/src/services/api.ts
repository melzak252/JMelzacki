import axios from 'axios';
import config from '../config.json';
import { User } from '../stores/auth';

console.log(config.version);
const apiClient = axios.create({
  baseURL: config.apiUrl,
  withCredentials: true,   // Include credentials for cross-origin requests
  headers: {
    "Content-Type": "application/json", // Form-encoded data for auth
  },
});

const authClient = axios.create({
  baseURL: config.apiUrl,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded", // Form-encoded data for auth
  },
});

apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API error:', error.response || error.message);
    if(error.status >= 500) return Promise.reject(error);

    return error.response
  }
);
// API service for the game
export const apiService = {
  async login(credentials: { username: string; password: string }) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return await authClient.post("/login", formData);
  },
  async logout(): Promise<{success: boolean}>{
    return await apiClient.post(`${config.apiUrl}/logout`, {},
    {
    withCredentials: true
    });
  },
  async getUser() {
    const response = await axios.get(`${config.apiUrl}/users/me`, {
    withCredentials: true
    });
    return response
  },
  googleSignIn(credential: string) {
    return apiClient.post("/google-signin", { credential: credential });
  },
  register(credentials: {username: string; email: string; password: string}) {
    return apiClient.post('/register', credentials);
  },
  getGameState() {
    return apiClient.get('/countrydle/state');
  },

  askQuestion(question: string) {
    return apiClient.post('/countrydle/question', { question });
  },

  makeGuess(guess: string) {
    return apiClient.post('/countrydle/guess', { guess });  // Submit a guess
  },

  endGame() {
    return apiClient.get('/countrydle/end');  // End the game and get the final result (country and explanations)
  },
  getCountrydleHistory() {
    return apiClient.get('/countrydle/history');  // End the game and get the final result (country and explanations)
  },
  updateUser(user: User) {
    return apiClient.post('/users/update', user);  // End the game and get the final result (country and explanations)
  },
  changePassword(password: string) {
    return apiClient.post('/users/change/password', { password });  // End the game and get the final result (country and explanations)
  },

};