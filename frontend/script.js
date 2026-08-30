// Use the config file for API base
const API_BASE = APP_CONFIG.API_BASE || 'http://127.0.0.1:8000';

let gameId = null;
let currentPuzzle = null;

// Rest of the code remains the same...
// (Keep all other code unchanged)

// DOM elements
const startScreen = document.getElementById('start-screen');
const gameScreen = document.getElementById('game-screen');
const completionScreen = document.getElementById('completion-screen');
const usernameInput = document.getElementById('username-input');
const startBtn = document.getElementById('start-btn');
const scoreDisplay = document.getElementById('score-display');
const inventoryDisplay = document.getElementById('inventory-display');
const puzzleTitle = document.getElementById('puzzle-title');
const puzzleDescription = document.getElementById('puzzle-description');
const puzzleInputArea = document.getElementById('puzzle-input-area');
const messageArea = document.getElementById('message-area');
const hintBtn = document.getElementById('hint-btn');
const restartBtn = document.getElementById('restart-btn');
const finalScore = document.getElementById('final-score');

// Helper functions
function showScreen(screen) {
    [startScreen, gameScreen, completionScreen].forEach(s => s.classList.remove('active'));
    screen.classList.add('active');
}

function displayMessage(text, type = 'info') {
    messageArea.textContent = text;
    messageArea.className = '';
    messageArea.classList.add(`message-${type}`);
}

function updateHUD(gameState) {
    scoreDisplay.textContent = `Score: ${gameState.score}`;
    const inv = gameState.inventory.length > 0 ? gameState.inventory.join(', ') : 'empty';
    inventoryDisplay.textContent = `Inventory: ${inv}`;
}

// API calls
async function apiCall(endpoint, method = 'GET', body = null) {
    const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
    };
    if (body) options.body = JSON.stringify(body);
    const response = await fetch(`${API_BASE}${endpoint}`, options);
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || 'Request failed');
    }
    return response.json();
}

// Start game
async function startGame() {
    const username = usernameInput.value.trim();
    if (!username) {
        alert('Please enter your name');
        return;
    }
    try {
        const game = await apiCall('/game/start', 'POST', { username });
        gameId = game.id;
        showScreen(gameScreen);
        await loadCurrentPuzzle();
    } catch (err) {
        alert('Error starting game: ' + err.message);
    }
}

// Load current puzzle
async function loadCurrentPuzzle() {
    if (!gameId) return;
    try {
        const puzzle = await apiCall(`/game/${gameId}/puzzle`);
        currentPuzzle = puzzle;
        renderPuzzle(puzzle);
        updateHUD(await apiCall(`/game/${gameId}`));
    } catch (err) {
        if (err.message.includes('completed')) {
            showCompletion();
        } else {
            displayMessage('Error loading puzzle: ' + err.message, 'error');
        }
    }
}

// Render puzzle based on type
function renderPuzzle(puzzle) {
    puzzleTitle.textContent = puzzle.title;
    puzzleDescription.textContent = puzzle.description;
    puzzleInputArea.innerHTML = '';
    messageArea.textContent = '';
    messageArea.className = '';

    switch (puzzle.puzzle_type) {
        case 'text':
        case 'code':
            puzzleInputArea.innerHTML = `
                <input type="text" id="answer-input" placeholder="Enter your answer" autocomplete="off">
                <button class="btn primary" id="submit-answer">Submit</button>
            `;
            document.getElementById('submit-answer').addEventListener('click', () => {
                const answer = document.getElementById('answer-input').value;
                submitAnswer(answer);
            });
            document.getElementById('answer-input').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') submitAnswer(document.getElementById('answer-input').value);
            });
            break;

        case 'multiple_choice':
            const options = puzzle.options || [];
            puzzleInputArea.innerHTML = `
                <div class="options-grid">
                    ${options.map(opt => `<button class="option-btn" data-value="${opt}">${opt}</button>`).join('')}
                </div>
                <button class="btn primary" id="submit-answer" style="margin-top:15px;">Submit</button>
            `;
            let selectedOption = null;
            document.querySelectorAll('.option-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    document.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    selectedOption = btn.dataset.value;
                });
            });
            document.getElementById('submit-answer').addEventListener('click', () => {
                if (selectedOption) submitAnswer(selectedOption);
            });
            break;

        case 'item_use':
            // For item_use, we just need a button to use the required item
            puzzleInputArea.innerHTML = `
                <p>You need to use an item to solve this puzzle.</p>
                <button class="btn primary" id="use-item-btn">Use Item</button>
            `;
            document.getElementById('use-item-btn').addEventListener('click', () => {
                // Determine which item to use (first required item in inventory)
                const requiredItem = puzzle.required_items[0];
                submitAnswer(requiredItem, requiredItem);
            });
            break;

        default:
            puzzleInputArea.innerHTML = `<p>Unknown puzzle type</p>`;
    }
}

// Submit answer
async function submitAnswer(answer, itemUsed = null) {
    if (!gameId) return;
    try {
        const body = { answer: answer };
        if (itemUsed) body.item_used = itemUsed;
        const result = await apiCall(`/game/${gameId}/solve`, 'POST', body);
        if (result.success) {
            displayMessage(result.message + ` (+${result.points_awarded} points)`, 'success');
            updateHUD({
                score: result.updated_score,
                inventory: result.updated_inventory
            });
            if (result.is_game_completed) {
                setTimeout(() => showCompletion(), 1500);
            } else {
                setTimeout(() => loadCurrentPuzzle(), 1500);
            }
        } else {
            displayMessage(result.message, 'error');
        }
    } catch (err) {
        displayMessage('Error: ' + err.message, 'error');
    }
}

// Get hint
async function getHint() {
    if (!gameId) return;
    try {
        const hint = await apiCall(`/game/${gameId}/hint`, 'POST');
        if (hint.success) {
            displayMessage(`Hint: ${hint.hint_text} (${hint.hints_remaining} remaining)`, 'info');
        } else {
            displayMessage(hint.message, 'error');
        }
    } catch (err) {
        displayMessage('Error: ' + err.message, 'error');
    }
}

// Show completion screen
async function showCompletion() {
    const gameState = await apiCall(`/game/${gameId}`);
    finalScore.textContent = `Final Score: ${gameState.score}`;
    showScreen(completionScreen);
}

// Restart game
function restartGame() {
    gameId = null;
    currentPuzzle = null;
    usernameInput.value = '';
    showScreen(startScreen);
}

// Event listeners
startBtn.addEventListener('click', startGame);
hintBtn.addEventListener('click', getHint);
restartBtn.addEventListener('click', restartGame);

// Initialize
showScreen(startScreen);
