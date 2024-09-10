import { defineStore } from 'pinia';
import { apiService } from '../services/api';

export interface User {
    username: string;
    email: string;
}

interface AuthState {
  user: User | null;
  isAuth: boolean;
  isGoogle: boolean;
  error: boolean;
  errorMessage: string;
}

export const useAuthStore = defineStore('auth', {
  // State section
  state: (): AuthState => ({
    user: null,
    isAuth: false,
    isGoogle: false,
    error: false,
    errorMessage: ''
  }),

  // Actions section
  actions: {
    async login(credentials: { username: string; password: string }) {        
        this.error = false;
        this.errorMessage = '';
        try {
            const response = await apiService.login(credentials);
            if(response.status !== 200) {
                this.error = true;
                this.errorMessage = response.data.detail;
                await this.logout()
                return;
            }
            this.user = response.data;
            this.isAuth = true;
            this.isGoogle = false;
        } catch(error: any) {
            this.error = true;
            this.errorMessage = error.response.data.detail;
            await this.logout()
            return;
        }
    },
    async logout() {
        this.isAuth = false;
        this.isGoogle = false;
        this.user = null;
        await apiService.logout();
    },
    async getUser() {
        this.error = false;
        this.errorMessage = '';

        const response = await apiService.getUser();
        if(response.status !== 200) {
            this.error = true;
            this.errorMessage = response.data.detail;
            this.logout()
            return;
        }

        const apiUser = response.data;

        if(!apiUser) {
            this.logout();
            return;
        }

        this.isAuth = true;
        this.user = apiUser;
    },
    async googleSignIn(credential: string) {
        try {
            const response = await apiService.googleSignIn(credential);
            if(response.status !== 200) {
                this.error = true;
                this.errorMessage = response.data.detail;
                this.logout();
                return;
            }
            this.user = response.data;
            this.isAuth = true;
            this.isGoogle = true;
        } catch (error: any) {
            this.error = true;
            this.errorMessage = error.response.data.detail;
            await this.logout()
        }
    }
  }
});
