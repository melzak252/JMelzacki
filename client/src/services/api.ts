import axios from 'axios';
import config from '../config.json';
// Create an axios instance for general API requests
const apiClient = axios.create({
  baseURL: config.apiUrl,
  withCredentials: true,   // Include credentials for cross-origin requests
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
    return Promise.reject(error);
  }
);
// API service for the game
export const apiService = {
  login(credentials: { username: string; password: string }) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    return authClient.post("/login", formData);
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
};