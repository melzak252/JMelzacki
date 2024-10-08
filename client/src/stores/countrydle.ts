import { defineStore } from 'pinia';
import { apiService } from '../services/api';

export interface Question {
  original_question: string;
  question: string;
  answer: boolean | null;
  valid: boolean;
  explanation?: string;
}

export interface Country { 
  name: string;
  official_name: string;
}

export interface GameState {
  questionsHistory: Array<Question>;
  guessHistory: Array<{
    guess: string;
    response: string;
  }>;
  selectedCountries: Array<string>;
  remainingQuestions: number;
  remainingGuesses: number;
  isGameOver: boolean;
  won: boolean;
  correctCountry: Country | null;
  questionLimitReached: boolean;
  guessLimitReached: boolean;
  loading: boolean;
  error: string | null;
  gameDate: string;
  countrydleHistory: Array<{
    date: string;
    country: Country;
  }>;
  countriesCount: Array<{
    name: string;
    count: number;
    last: string;
  }>;
}

export const useCountrydleStore = defineStore('countrydle', {
  // State section
  state: (): GameState => ({
    questionsHistory: [] as Array<Question>,
    selectedCountries: [] as Array<string>,
    guessHistory: [] as Array<{ guess: string; response: string; }>,
    remainingQuestions: 10,
    remainingGuesses: 3,
    isGameOver: false,
    won: false,
    correctCountry: null,  
    questionLimitReached: false,
    guessLimitReached: false, 
    loading: false,  
    error: null,  
    gameDate: '',
    countrydleHistory: [],
    countriesCount: [],
  }),

  // Actions section
  actions: {
    async loadGameState() {
      this.resetCorrect();

      const today = new Date().toISOString().split('T')[0];  
      if (this.gameDate !== today)   
        this.resetState()



      this.loading = true;
      try {
        const response = await apiService.getGameState();  
        this.questionsHistory = response.data.questions_history;
        this.guessHistory = response.data.guess_history;
        this.remainingQuestions = response.data.remaining_questions;
        this.remainingGuesses = response.data.remaining_guesses;
        this.isGameOver = response.data.is_game_over;
        this.won = response.data.won;
        this.gameDate = response.data.date;

        if(this.isGameOver) this.endGame()
      } catch (err) {
        this.error = 'Failed to load the game state.';
        this.resetState();
      } finally {
        this.loading = false;
      }
    },

    async askQuestion(question: string) {
      if (this.remainingQuestions <= 0 || this.isGameOver) return;

      this.loading = true;
      try {
        const response = await apiService.askQuestion(question);  
        this.questionsHistory.push({ ...response.data });
        this.remainingQuestions--;
      } catch (err) {
        this.error = 'Failed to ask the question.';
      } finally {
        this.loading = false;
      }
    },
    async makeGuess(guess: string) {
      if (this.remainingGuesses <= 0 || this.isGameOver) return;

      this.loading = true;
      try {
        const response = await apiService.makeGuess(guess);  
        this.guessHistory.push({ guess, response: response.data.response });
        this.remainingGuesses--;

        if (response.data.response === 'True' || this.remainingGuesses <= 0) {
          await this.endGame();
        }
      } catch (err) {
        this.error = 'Failed to submit the guess.';
      } finally {
        this.loading = false;
      }
    },

    async endGame() {
      this.loading = true;
      try {
        const response = await apiService.endGame();  
        this.correctCountry = response.data.country;
        this.questionsHistory = response.data.questions_history;
        this.guessHistory = response.data.guess_history;
        this.remainingQuestions = response.data.remaining_questions;
        this.remainingGuesses = response.data.remaining_guesses;
        this.won = response.data.won;
        this.isGameOver = true;
      } catch (err) {
        this.error = 'Failed to end the game.';
      } finally {
        this.loading = false;
      }
    },
    handleCountryClick(countryName: string) {
      const index = this.selectedCountries.indexOf(countryName);
      if (index === -1) {
        this.selectedCountries.push(countryName);
        return true;
      } else {
        this.selectedCountries.splice(index, 1);
        return false;
      }
    },
    resetState() {
      this.questionsHistory = [];
      this.guessHistory = [];
      this.selectedCountries = [];
      this.remainingQuestions = 10;
      this.remainingGuesses = 3;
      this.isGameOver = false;
      this.won = false;
      this.correctCountry = null;
    },
    resetCorrect() {
      this.isGameOver = false;
      this.won = false;
      this.correctCountry = null;
    },
    async getCountrydleHistory() {
      this.loading = true;
      try {
        const response = await apiService.getCountrydleHistory();
        this.countrydleHistory = response.data.daily_countries;
        this.countriesCount = response.data.countries_count;
      } catch (err) {
        this.error = 'Failed to load the countrydle history.';
      } finally {
        this.loading = false;
      }
    },
  },

  persist: {
    storage: localStorage,
  },
});
