import { ref } from 'vue';
import axios from 'axios';
export function useGame() {
    const maxQuestions = 10;
    const maxGuesses = 3;

    const questionsAsked = ref(0);
    const guessesMade = ref(0);
    const isGameOver = ref(false);
    const remainingQuestions = ref(maxQuestions);
    const remainingGuesses = ref(maxGuesses);
    const questionsHistory = ref<Array<{ question: string; answer: string }>>([]);
    const guessHistory = ref<Array<{ guess: string; response: string }>>([]);
    const loading = ref(false); // New loading state
    const error = ref<string | null>(null); // Error handling state
    const won = ref<boolean>(false);
    // Function to ask a question and update the state
    const askQuestion = async (question: string) => {
        if (questionsAsked.value < maxQuestions && !isGameOver.value) {
            loading.value = true;
            error.value = null;

            try {
                const response = await axios.post('https://jmelzacki.com/api/game/question', { question: question },
                    {
                        withCredentials: true
                    });
                const answer = response.data.answer;

                questionsHistory.value.push({ question, answer });
                questionsAsked.value++;
                remainingQuestions.value = maxQuestions - questionsAsked.value;
            } catch (err) {
                error.value = 'Failed to fetch the answer. Please try again.';
            } finally {
                loading.value = false;
            }
        }
    };

    const getUserTodayHistory = async () => {

        try {
            loading.value = true;
            error.value = null;
            const response = await axios.get('https://jmelzacki.com/api/game/history',
                {
                    withCredentials: true
                });
            const data = response.data;

            questionsHistory.value = data.questions;
            guessHistory.value = data.guesses;
            guessesMade.value = guessHistory.value.length;
            questionsAsked.value = questionsHistory.value.length;
            remainingQuestions.value = maxGuesses - questionsAsked.value;
            remainingGuesses.value = maxGuesses - guessesMade.value;

            won.value = guessHistory.value.some((obj) => obj.response.toLocaleLowerCase() === "true")
            isGameOver.value = remainingGuesses.value <= 0 || won.value
            
        }catch (err) {
                error.value = 'Failed to connect with server. Please try again.';
            } finally {
                loading.value = false;
            }
    }
    // Function to make a guess and update the state
    const makeGuess = async (guess: string) => {
        if (guessesMade.value < maxGuesses && !isGameOver.value) {
            loading.value = true;
            error.value = null;

            try {
                // Simulate an API call to check if the guess is correct
                const res = await axios.post('https://jmelzacki.com/api/game/guess', { guess: guess },
                    {
                        withCredentials: true
                    });

                const response = res.data.response;

                guessHistory.value.push({ guess, response});
                guessesMade.value++;
                remainingGuesses.value = maxGuesses - guessesMade.value;

                if (guessesMade.value >= maxGuesses || response === "True") {
                    isGameOver.value = true;
                    won.value = response === "True"
                }
            } catch (err) {
                error.value = 'Failed to check the guess. Please try again.';
            } finally {
                loading.value = false;
            }
        }
    };

    // Function to reset the game state
    const resetGame = () => {
        questionsAsked.value = 0;
        guessesMade.value = 0;
        remainingQuestions.value = maxQuestions;
        remainingGuesses.value = maxGuesses;
        isGameOver.value = false;
        guessHistory.value = [];
        questionsHistory.value = [];
        loading.value = false;
        error.value = null;
    };

    return {
        questionsAsked,
        guessesMade,
        remainingQuestions,
        remainingGuesses,
        isGameOver,
        questionsHistory,
        guessHistory,
        loading,
        error,
        won,
        askQuestion,
        makeGuess,
        resetGame,
        getUserTodayHistory
    };
}
