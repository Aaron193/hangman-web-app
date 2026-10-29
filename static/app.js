const form = document.querySelector('#new-game-form');
const difficulty = document.querySelector('#difficulty');
const newGame = document.querySelector('#new-game');
const statusArea = document.querySelector('#status');
const pattern = document.querySelector('#pattern');
const remaining = document.querySelector('#remaining');
const guessed = document.querySelector('#guessed');
const incorrect = document.querySelector('#incorrect');
const parts = document.querySelectorAll('.parts > *');
const keyboard = document.querySelector('#keyboard');
let game = null;
let pending = false;
let gameGone = false;

for (const letter of 'abcdefghijklmnopqrstuvwxyz') {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = letter.toUpperCase();
  button.dataset.letter = letter;
  button.addEventListener('click', () => submitGuess(letter));
  keyboard.appendChild(button);
}

function showStatus(message, kind = '') {
  statusArea.textContent = message;
  statusArea.classList.remove('error', 'won', 'lost');
  if (kind) statusArea.classList.add(kind);
}

function render() {
  newGame.disabled = pending;
  difficulty.disabled = pending;
  pattern.textContent = game ? game.pattern : '—';
  remaining.textContent = game ? game.remaining_guesses : '—';
  guessed.textContent = game && game.guessed_letters.length ? game.guessed_letters.join(', ').toUpperCase() : 'None yet';
  incorrect.textContent = game && game.incorrect_letters.length ? game.incorrect_letters.join(', ').toUpperCase() : 'None yet';
  parts.forEach((part, index) => { part.toggleAttribute('hidden', !game || index >= game.incorrect_letters.length); });
  for (const button of keyboard.children) {
    const letter = button.dataset.letter;
    const wasGuessed = Boolean(game && game.guessed_letters.includes(letter));
    const wasWrong = Boolean(game && game.incorrect_letters.includes(letter));
    button.disabled = pending || gameGone || !game || game.status !== 'playing' || wasGuessed;
    button.classList.toggle('right', wasGuessed && !wasWrong);
    button.classList.toggle('wrong', wasWrong);
    button.setAttribute('aria-label', `${letter.toUpperCase()}${wasGuessed ? (wasWrong ? ', wrong' : ', correct') : ''}`);
  }
}

async function requestGame(url, body, isGuess = false) {
  if (pending) return;
  pending = true;
  let focusNewGame = false;
  showStatus('Working...');
  render();
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      if (isGuess && response.status === 404) {
        gameGone = true;
        showStatus('This game is gone. Start a new game to play again.', 'error');
      } else {
        showStatus(data.error || `Request failed (${response.status}). Please try again.`, 'error');
      }
      return;
    }
    game = data;
    gameGone = false;
    if (game.status === 'won' || game.status === 'lost') {
      const outcome = game.status === 'won' ? 'You won!' : 'You lost.';
      showStatus(game.word ? `${outcome} The word was ${game.word}.` : outcome, game.status);
      focusNewGame = true;
    } else {
      showStatus('');
    }
  } catch (error) {
    showStatus('Network error. Please check your connection and try again.', 'error');
  } finally {
    pending = false;
    render();
    if (focusNewGame) newGame.focus();
  }
}

form.addEventListener('submit', event => {
  event.preventDefault();
  requestGame('/api/games', { difficulty: difficulty.value });
});

function submitGuess(letter) {
  if (pending || gameGone || !game || game.status !== 'playing' || game.guessed_letters.includes(letter)) return;
  requestGame(`/api/games/${encodeURIComponent(game.game_id)}/guess`, { letter }, true);
}

document.addEventListener('keydown', event => {
  if (event.ctrlKey || event.altKey || event.metaKey || event.repeat || (event.target instanceof Element && event.target.closest('select, input, textarea'))) return;
  if (/^[a-z]$/i.test(event.key)) submitGuess(event.key.toLowerCase());
});

render();
requestGame('/api/games', { difficulty: difficulty.value });
