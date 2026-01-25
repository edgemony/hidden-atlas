// Game state
let gameState = {
    currentLevel: 1,
    attempts: 0,
    maxAttempts: 5,
    guesses: [],
    gameOver: false,
    won: false,
    correctCity: null,
    todayDate: null,
    bonusRoundComplete: false
};

// Get today's date in YYYY-MM-DD format (UTC)
function getTodayDate() {
    const now = new Date();
    return now.toISOString().split('T')[0];
}

// Load game state from localStorage
function loadGameState() {
    const today = getTodayDate();
    const saved = localStorage.getItem('citydleState');

    if (saved) {
        const savedState = JSON.parse(saved);
        // Check if it's from today
        if (savedState.todayDate === today) {
            gameState = savedState;
            return true;
        }
    }

    // New game
    gameState.todayDate = today;
    return false;
}

// Save game state to localStorage
function saveGameState() {
    localStorage.setItem('citydleState', JSON.stringify(gameState));
}

// Fetch the current city data
async function fetchCityData() {
    try {
        // For now, using a placeholder structure
        // In production, this would fetch from your API or static JSON
        const response = await fetch(`/maps/${gameState.todayDate}/city.json`);
        if (!response.ok) {
            // Fallback for development
            return {
                name: "Portland",
                state: "Oregon",
                country: "USA"
            };
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching city data:', error);
        // Fallback for development
        return {
            name: "Portland",
            state: "Oregon",
            country: "USA"
        };
    }
}

// Load map image for current level
function loadMapImage() {
    const mapImage = document.getElementById('map-image');
    const loading = document.getElementById('loading');

    loading.style.display = 'block';
    mapImage.classList.remove('loaded');

    // Map image path: /maps/YYYY-MM-DD/level1.png
    const imagePath = `/maps/${gameState.todayDate}/level${gameState.currentLevel}.png`;

    mapImage.onload = () => {
        loading.style.display = 'none';
        mapImage.classList.add('loaded');
    };

    mapImage.onerror = () => {
        loading.textContent = 'Map not available';
        console.error('Failed to load map:', imagePath);
    };

    mapImage.src = imagePath;
    mapImage.alt = `City map - Level ${gameState.currentLevel}`;
}

// Update UI
function updateUI() {
    document.getElementById('attempt').textContent = `${gameState.attempts}/${gameState.maxAttempts}`;
    document.getElementById('level').textContent = gameState.currentLevel;

    // Update guesses list
    const guessesList = document.getElementById('guesses');
    guessesList.innerHTML = '';
    gameState.guesses.forEach((guess, index) => {
        const li = document.createElement('li');
        li.textContent = `${index + 1}. ${guess}`;
        guessesList.appendChild(li);
    });

    // Disable input if game is over
    const input = document.getElementById('city-input');
    const submitBtn = document.getElementById('submit-btn');
    if (gameState.gameOver) {
        input.disabled = true;
        submitBtn.disabled = true;
    }
}

// Normalize city name for comparison
function normalizeCity(name) {
    return name.toLowerCase()
        .trim()
        .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, '')
        .replace(/\s+/g, ' ');
}

// Check if guess is correct
function checkGuess(guess, correctCity) {
    const normalizedGuess = normalizeCity(guess);
    const normalizedCity = normalizeCity(correctCity.name);

    // Exact match
    if (normalizedGuess === normalizedCity) {
        return true;
    }

    // Check with state/country variations
    const withState = normalizeCity(`${correctCity.name} ${correctCity.state || ''}`);
    const withCountry = normalizeCity(`${correctCity.name} ${correctCity.country || ''}`);

    return normalizedGuess === withState || normalizedGuess === withCountry;
}

// Show message
function showMessage(text, type = '') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = text;
    messageEl.className = `message ${type}`;

    if (type) {
        setTimeout(() => {
            messageEl.className = 'message';
            messageEl.textContent = '';
        }, 3000);
    }
}

// Update hints based on current level
function updateHints() {
    const hintsPanel = document.getElementById('hints-panel');
    const hint1 = document.getElementById('hint-1');
    const hint2 = document.getElementById('hint-2');
    const continentEl = document.getElementById('hint-continent');
    const countryEl = document.getElementById('hint-country');

    // Show hints panel if any hints are visible
    const showPanel = gameState.currentLevel >= 3;
    hintsPanel.classList.toggle('hidden', !showPanel);

    // Hint 1: Continent (shown at level 3+, after 2nd wrong guess)
    if (gameState.currentLevel >= 3 && gameState.correctCity?.continent) {
        hint1.classList.remove('hidden');
        continentEl.textContent = gameState.correctCity.continent;
    } else {
        hint1.classList.add('hidden');
    }

    // Hint 2: Country (shown at level 5, after 4th wrong guess)
    if (gameState.currentLevel >= 5 && gameState.correctCity?.country) {
        hint2.classList.remove('hidden');
        countryEl.textContent = gameState.correctCity.country;
    } else {
        hint2.classList.add('hidden');
    }
}

// Reset hints to hidden state
function resetHints() {
    const hintsPanel = document.getElementById('hints-panel');
    const hint1 = document.getElementById('hint-1');
    const hint2 = document.getElementById('hint-2');

    hintsPanel.classList.add('hidden');
    hint1.classList.add('hidden');
    hint2.classList.add('hidden');
}

// Handle guess submission
async function handleGuess() {
    const input = document.getElementById('city-input');
    const guess = input.value.trim();

    if (!guess) {
        showMessage('Please enter a city name', 'error');
        return;
    }

    if (!gameState.correctCity) {
        gameState.correctCity = await fetchCityData();
    }

    gameState.attempts++;
    gameState.guesses.push(guess);

    const isCorrect = checkGuess(guess, gameState.correctCity);

    if (isCorrect) {
        // Win!
        gameState.won = true;
        gameState.gameOver = true;
        showGameOver();
    } else if (gameState.attempts >= gameState.maxAttempts) {
        // Lost
        gameState.gameOver = true;
        showGameOver();
    } else {
        // Wrong guess, advance to next level
        gameState.currentLevel = Math.min(gameState.currentLevel + 1, 5);
        loadMapImage();
        updateHints();
        showMessage('Not quite! Try again with more detail...', 'error');
    }

    input.value = '';
    updateUI();
    saveGameState();
}

// Show game over screen
function showGameOver() {
    const gameOverEl = document.getElementById('game-over');
    const titleEl = document.getElementById('game-over-title');
    const messageEl = document.getElementById('game-over-message');
    const correctCityEl = document.getElementById('correct-city');

    if (gameState.won) {
        titleEl.textContent = 'Well done!';
        titleEl.className = 'won';
        messageEl.textContent = `You guessed the city in ${gameState.attempts} ${gameState.attempts === 1 ? 'try' : 'tries'}!`;
    } else {
        titleEl.textContent = 'Game Over';
        titleEl.className = 'lost';
        messageEl.textContent = 'Better luck tomorrow!';
    }

    const cityName = gameState.correctCity.state
        ? `${gameState.correctCity.name}, ${gameState.correctCity.state}`
        : gameState.correctCity.name;
    correctCityEl.textContent = cityName;

    gameOverEl.classList.remove('hidden');
    updateCountdown();

    // Show bonus round if population data is available
    const bonusRoundEl = document.getElementById('bonus-round');
    if (gameState.correctCity.population) {
        bonusRoundEl.classList.remove('hidden');
        // Restore bonus round if already completed
        restoreBonusRound();
    }
}

// Share results
function shareResults() {
    const emoji = gameState.won ? '🎯' : '❌';
    let text = `Citydle ${gameState.todayDate}\n${emoji} ${gameState.attempts}/${gameState.maxAttempts}`;

    // Add bonus round result if completed
    if (gameState.bonusRoundComplete && gameState.bonusAccuracy) {
        const bonusEmoji = {
            'excellent': '🎯',
            'good': '👍',
            'close': '🤔',
            'far': '📊'
        }[gameState.bonusAccuracy];
        text += `\nBonus: ${bonusEmoji}`;
    }

    text += `\n\nPlay at: ${window.location.href}`;

    if (navigator.share) {
        navigator.share({
            text: text
        }).catch(err => console.log('Share failed:', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.getElementById('share-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    }
}

// Parse population input (handles formats like "500000", "500,000", "500k", "1.5m")
function parsePopulationInput(input) {
    if (!input) return NaN;

    // Remove whitespace and convert to lowercase
    let cleaned = input.trim().toLowerCase();

    // Remove commas
    cleaned = cleaned.replace(/,/g, '');

    // Handle k/m suffixes
    let multiplier = 1;
    if (cleaned.endsWith('k')) {
        multiplier = 1000;
        cleaned = cleaned.slice(0, -1);
    } else if (cleaned.endsWith('m')) {
        multiplier = 1000000;
        cleaned = cleaned.slice(0, -1);
    }

    const num = parseFloat(cleaned);
    return isNaN(num) ? NaN : Math.round(num * multiplier);
}

// Calculate accuracy class based on percentage difference
function getAccuracyClass(guessed, actual) {
    const percentOff = Math.abs(guessed - actual) / actual;

    if (percentOff <= 0.10) return 'excellent';
    if (percentOff <= 0.25) return 'good';
    if (percentOff <= 0.50) return 'close';
    return 'far';
}

// Get feedback message based on accuracy
function getBonusFeedback(guessed, actual, accuracyClass) {
    const diff = guessed - actual;
    const percentOff = Math.round(Math.abs(diff) / actual * 100);
    const direction = diff > 0 ? 'high' : 'low';
    const actualFormatted = actual.toLocaleString();

    switch (accuracyClass) {
        case 'excellent':
            return `🎯 Excellent! The population is ${actualFormatted}. You were only ${percentOff}% off!`;
        case 'good':
            return `👍 Good guess! The population is ${actualFormatted}. You were ${percentOff}% ${direction}.`;
        case 'close':
            return `🤔 Close! The population is ${actualFormatted}. You were ${percentOff}% ${direction}.`;
        case 'far':
            return `📊 The population is ${actualFormatted}. You were ${percentOff}% ${direction}.`;
    }
}

// Handle bonus round population guess
function handleBonusGuess() {
    const input = document.getElementById('population-input');
    const submitBtn = document.getElementById('population-submit');
    const resultEl = document.getElementById('bonus-result');

    const guessedPop = parsePopulationInput(input.value);

    if (isNaN(guessedPop) || guessedPop <= 0) {
        resultEl.textContent = 'Please enter a valid number';
        resultEl.className = 'bonus-result';
        return;
    }

    const actualPop = gameState.correctCity.population;
    const accuracyClass = getAccuracyClass(guessedPop, actualPop);
    const feedback = getBonusFeedback(guessedPop, actualPop, accuracyClass);

    // Display result
    resultEl.textContent = feedback;
    resultEl.className = `bonus-result ${accuracyClass}`;

    // Update state
    gameState.bonusRoundComplete = true;
    gameState.bonusGuess = guessedPop;
    gameState.bonusAccuracy = accuracyClass;
    saveGameState();

    // Disable input
    input.disabled = true;
    submitBtn.disabled = true;
}

// Restore bonus round state if already completed
function restoreBonusRound() {
    if (!gameState.bonusRoundComplete || !gameState.correctCity.population) return;

    const input = document.getElementById('population-input');
    const submitBtn = document.getElementById('population-submit');
    const resultEl = document.getElementById('bonus-result');

    const actualPop = gameState.correctCity.population;
    const guessedPop = gameState.bonusGuess;
    const accuracyClass = gameState.bonusAccuracy;
    const feedback = getBonusFeedback(guessedPop, actualPop, accuracyClass);

    // Show previous result
    input.value = guessedPop.toLocaleString();
    input.disabled = true;
    submitBtn.disabled = true;
    resultEl.textContent = feedback;
    resultEl.className = `bonus-result ${accuracyClass}`;
}

// Setup bonus round event listeners
function setupBonusRound() {
    const submitBtn = document.getElementById('population-submit');
    const input = document.getElementById('population-input');

    submitBtn.addEventListener('click', handleBonusGuess);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !gameState.bonusRoundComplete) {
            handleBonusGuess();
        }
    });
}

// Update countdown to next game
function updateCountdown() {
    const countdownEl = document.getElementById('countdown');

    function update() {
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
        tomorrow.setUTCHours(0, 0, 0, 0);

        const diff = tomorrow - now;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        countdownEl.textContent = `${hours}h ${minutes}m ${seconds}s`;
    }

    update();
    setInterval(update, 1000);
}

// Show all maps grid
function showAllMaps() {
    const modal = document.getElementById('all-maps-modal');

    // Load all map images
    for (let level = 1; level <= 5; level++) {
        const img = modal.querySelector(`[data-level="${level}"] img`);
        img.src = `/maps/${gameState.todayDate}/level${level}.png`;
    }

    modal.classList.remove('hidden');
}

// Show zoomed map
function showZoomedMap(level) {
    const modal = document.getElementById('map-zoom-modal');
    const title = document.getElementById('zoom-title');
    const image = document.getElementById('zoom-image');

    title.textContent = `Level ${level}`;
    image.src = `/maps/${gameState.todayDate}/level${level}.png`;

    modal.classList.remove('hidden');
}

// Setup all maps modal
function setupAllMapsModal() {
    const modal = document.getElementById('all-maps-modal');
    const btn = document.getElementById('view-all-btn');
    const close = modal.querySelector('.close');
    const mapItems = modal.querySelectorAll('.map-item');

    btn.addEventListener('click', showAllMaps);

    close.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });

    // Click on map item to zoom
    mapItems.forEach(item => {
        item.addEventListener('click', () => {
            const level = item.dataset.level;
            showZoomedMap(level);
        });
    });
}

// Setup map zoom modal
function setupMapZoomModal() {
    const modal = document.getElementById('map-zoom-modal');
    const close = modal.querySelector('.close');

    close.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

// Help modal
function setupHelpModal() {
    const modal = document.getElementById('help-modal');
    const btn = document.getElementById('help-btn');
    const close = modal.querySelector('.close');

    btn.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    close.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

// Reset game for replay
function resetGame() {
    // Reset game state
    gameState.currentLevel = 1;
    gameState.attempts = 0;
    gameState.guesses = [];
    gameState.gameOver = false;
    gameState.won = false;
    gameState.bonusRoundComplete = false;
    gameState.bonusGuess = null;
    gameState.bonusAccuracy = null;

    // Save reset state
    saveGameState();

    // Hide game over modal
    document.getElementById('game-over').classList.add('hidden');

    // Re-enable inputs
    const input = document.getElementById('city-input');
    const submitBtn = document.getElementById('submit-btn');
    input.disabled = false;
    submitBtn.disabled = false;

    // Reset bonus round inputs
    const bonusRoundEl = document.getElementById('bonus-round');
    const bonusInput = document.getElementById('population-input');
    const bonusSubmitBtn = document.getElementById('population-submit');
    const bonusResult = document.getElementById('bonus-result');
    bonusRoundEl.classList.add('hidden');
    bonusInput.value = '';
    bonusInput.disabled = false;
    bonusSubmitBtn.disabled = false;
    bonusResult.textContent = '';
    bonusResult.className = 'bonus-result';

    // Reset hints
    resetHints();

    // Reset UI
    updateUI();

    // Load level 1 map
    loadMapImage();

    // Clear message
    document.getElementById('message').textContent = '';
    document.getElementById('message').className = 'message';

    // Focus input
    input.focus();
}

// Initialize game
async function initGame() {
    // Load saved state
    loadGameState();

    // Fetch correct city
    gameState.correctCity = await fetchCityData();

    // Load map
    loadMapImage();

    // Update UI
    updateUI();

    // Update hints based on current level
    updateHints();

    // Show game over if already finished
    if (gameState.gameOver) {
        showGameOver();
    }

    // Setup event listeners
    const submitBtn = document.getElementById('submit-btn');
    const input = document.getElementById('city-input');

    submitBtn.addEventListener('click', handleGuess);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !gameState.gameOver) {
            handleGuess();
        }
    });

    document.getElementById('share-btn').addEventListener('click', shareResults);
    document.getElementById('replay-btn').addEventListener('click', resetGame);

    setupHelpModal();
    setupAllMapsModal();
    setupMapZoomModal();
    setupBonusRound();

    // Focus input
    if (!gameState.gameOver) {
        input.focus();
    }
}

// Start the game when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGame);
} else {
    initGame();
}
