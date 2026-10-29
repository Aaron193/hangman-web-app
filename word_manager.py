"""Load and select words for each hangman difficulty."""

from pathlib import Path
import random
import re


class WordManager:
    """Load validated word lists and choose words using an injectable generator."""

    DIFFICULTIES = ("easy", "medium", "hard")

    def __init__(self, words_dir=None, rng=None):
        self.words_dir = Path(words_dir) if words_dir is not None else Path(__file__).resolve().parent / "words"
        self.rng = rng if rng is not None else random.Random()
        self.words = {difficulty: self._load(difficulty) for difficulty in self.DIFFICULTIES}

    def _load(self, difficulty):
        path = self.words_dir / f"{difficulty}.txt"
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError as exc:
            raise ValueError(f"Word list file not found: {path}") from exc

        words = []
        seen = set()
        for line in lines:
            word = line.strip().lower()
            if not word:
                continue
            if re.fullmatch(r"[a-z]+", word) is None:
                raise ValueError(f"Invalid entry {word!r} in word list {path}")
            if word not in seen:
                seen.add(word)
                words.append(word)
        if not words:
            raise ValueError(f"Word list is empty: {path}")
        return words

    def get_random_word(self, difficulty):
        """Return a random word for exactly one of the supported difficulties."""
        if not isinstance(difficulty, str) or difficulty not in self.DIFFICULTIES:
            raise ValueError(f"Invalid difficulty: {difficulty!r}")
        return self.rng.choice(self.words[difficulty])
