"""Hangman rules and state, independent of the web server."""

import re


class GameError(ValueError):
    """Base class for rejected guesses."""


class InvalidGuessError(GameError):
    """A guess is not a single ASCII letter."""


class GameOverError(GameError):
    """A guess was made after the game ended."""


class DuplicateGuessError(GameError):
    """A letter was already guessed."""


class HangmanGame:
    """A single game with six allowed incorrect guesses."""

    def __init__(self, word, difficulty, game_id):
        if not isinstance(word, str) or re.fullmatch(r"[a-zA-Z]+", word) is None:
            raise ValueError("Word must contain only ASCII letters and be non-empty")
        self._word = word.lower()
        self.difficulty = difficulty
        self.game_id = game_id
        self._guessed_letters = []
        self._incorrect_letters = []

    @property
    def guessed_letters(self):
        return self._guessed_letters.copy()

    @property
    def incorrect_letters(self):
        return self._incorrect_letters.copy()

    @property
    def remaining_guesses(self):
        return 6 - len(self._incorrect_letters)

    @property
    def status(self):
        if all(letter in self._guessed_letters for letter in self._word):
            return "won"
        if self.remaining_guesses == 0:
            return "lost"
        return "playing"

    @property
    def pattern(self):
        return " ".join(letter if letter in self._guessed_letters else "_" for letter in self._word)

    def guess(self, letter):
        if not isinstance(letter, str) or re.fullmatch(r"[a-zA-Z]", letter) is None:
            raise InvalidGuessError("Guess must be one ASCII letter")
        if self.status != "playing":
            raise GameOverError("Game is already over")
        letter = letter.lower()
        if letter in self._guessed_letters:
            raise DuplicateGuessError("Letter has already been guessed")
        self._guessed_letters.append(letter)
        if letter in self._word:
            return True
        self._incorrect_letters.append(letter)
        return False

    def to_dict(self):
        state = {
            "game_id": self.game_id,
            "difficulty": self.difficulty,
            "pattern": self.pattern,
            "guessed_letters": self.guessed_letters,
            "incorrect_letters": self.incorrect_letters,
            "remaining_guesses": self.remaining_guesses,
            "status": self.status,
        }
        if state["status"] != "playing":
            state["word"] = self._word
        return state
