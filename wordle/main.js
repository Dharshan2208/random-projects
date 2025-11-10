async function loadDictionary(filePath) {
  try {
    const response = await fetch(filePath);
    const text = await response.text();
    return text
      .split("\n")
      .map((word) => word.trim())
      .filter((word) => word);
  } catch (error) {
    console.error(`Error loading dictionary from ${filePath}:`, error);
    return [];
  }
}

function isValidGuess(guess, guesses) {
  return guesses.includes(guess);
}

function evaluateGuess(guess, word) {
  let result = "";

  for (let i = 0; i < 5; i++) {
    if (guess[i] === word[i]) {
      result += `<span style="color: green">${guess[i]}</span>`;
    } else if (word.includes(guess[i])) {
      result += `<span style="color: orange">${guess[i]}</span>`;
    } else {
      result += guess[i];
    }
  }

  return result;
}

function wordle(guesses, answers) {
  const gameContainer = document.getElementById("game-container");
  const feedbackArea = document.getElementById("feedback-area");
  const guessInput = document.getElementById("guess-input");
  const guessButton = document.getElementById("guess-button");
  const messageArea = document.getElementById("message-area");

  const secretWord = answers[Math.floor(Math.random() * answers.length)];
  let attempts = 1;
  const maxAttempts = 6;

  messageArea.textContent =
    "Welcome to Wordle! You have 6 chances to guess the word...";

  // Handle guesses
  guessButton.addEventListener("click", makeGuess);
  guessInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") makeGuess();
  });

  function makeGuess() {
    const guess = guessInput.value.toLowerCase().trim();

    // Input validation
    if (guess.length !== 5) {
      messageArea.textContent = "Please enter a 5-letter word!";
      return;
    }

    if (!isValidGuess(guess, guesses)) {
      messageArea.textContent = "Baka..Invalid Word";
      return;
    }

    // Process valid guess
    const attemptDiv = document.createElement("div");
    attemptDiv.className = "attempt";
    attemptDiv.innerHTML = `<span class="attempt-number">Guess #${attempts}: </span>`;

    if (guess === secretWord) {
      attemptDiv.innerHTML += `<span style="color: green">${guess}</span>`;
      feedbackArea.appendChild(attemptDiv);
      messageArea.textContent = `Congratulations!!! You guessed the word: ${secretWord}`;
      endGame();
    } else {
      attemptDiv.innerHTML += evaluateGuess(guess, secretWord);
      feedbackArea.appendChild(attemptDiv);

      attempts++;
      guessInput.value = "";

      if (attempts > maxAttempts) {
        messageArea.textContent = `Game Over!!! The word was: ${secretWord}`;
        endGame();
      }
    }
  }

  function endGame() {
    guessInput.disabled = true;
    guessButton.disabled = true;

    // Add reset button
    const resetButton = document.createElement("button");
    resetButton.textContent = "Play Again";
    resetButton.addEventListener("click", () => {
      location.reload();
    });
    gameContainer.appendChild(resetButton);
  }
}

async function initGame() {
  try {
    const guesses = await loadDictionary("guesses.txt");
    const answers = await loadDictionary("answers.txt");

    if (guesses.length === 0 || answers.length === 0) {
      const sampleWords = [
        "apple",
        "baker",
        "camel",
        "drums",
        "eagle",
        "false",
        "ghost",
        "hotel",
        "igloo",
        "joker",
      ];
      wordle(sampleWords, sampleWords);
    } else {
      wordle(guesses, answers);
    }
  } catch (error) {
    console.error("Error initializing game:", error);
    document.getElementById("message-area").textContent =
      "Error loading game resources!";
  }
}

initGame();
