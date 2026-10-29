import pytest

from game import DuplicateGuessError, GameError, GameOverError, HangmanGame, InvalidGuessError


@pytest.mark.parametrize("word", [None, 1, "", " ", "two words", "cat1", "cat-", "café", "cat\n"])
def test_invalid_words(word):
    with pytest.raises(ValueError):
        HangmanGame(word, "easy", "id")


def test_guesses_pattern_and_serialization():
    game = HangmanGame("BaNaNa", "medium", "game-1")
    assert game.to_dict() == {
        "game_id": "game-1", "difficulty": "medium", "pattern": "_ _ _ _ _ _",
        "guessed_letters": [], "incorrect_letters": [], "remaining_guesses": 6,
        "status": "playing",
    }
    assert game.guess("A") is True
    assert game.pattern == "_ a _ a _ a"
    assert game.guess("X") is False
    assert game.guess("b") is True
    assert game.to_dict() == {
        "game_id": "game-1", "difficulty": "medium", "pattern": "b a _ a _ a",
        "guessed_letters": ["a", "x", "b"], "incorrect_letters": ["x"],
        "remaining_guesses": 5, "status": "playing",
    }
    game.to_dict()["guessed_letters"].clear()
    game.incorrect_letters.clear()
    assert game.guessed_letters == ["a", "x", "b"]
    assert game.remaining_guesses == 5


@pytest.mark.parametrize("invalid", [None, 1, True, [], {}, "", "ab", "1", "!", " ", "é", "\n", "a\n", "Ａ"])
def test_invalid_guesses_leave_state_unchanged(invalid):
    game = HangmanGame("cat", "easy", "id")
    before = game.to_dict()
    with pytest.raises(InvalidGuessError):
        game.guess(invalid)
    assert game.to_dict() == before


@pytest.mark.parametrize("letter", ["a", "x"])
def test_duplicate_case_insensitive_does_not_change_state(letter):
    game = HangmanGame("cat", "easy", "id")
    game.guess(letter)
    before = game.to_dict()
    with pytest.raises(DuplicateGuessError):
        game.guess(letter.upper())
    assert game.to_dict() == before


@pytest.mark.parametrize("outcome, guesses", [("won", "cat"), ("lost", "bdefgh")])
def test_finished_games_and_word_disclosure(outcome, guesses):
    game = HangmanGame("cat", "easy", "id")
    assert "cat" not in str(game.to_dict())
    assert "cat" not in repr(game)
    for letter in guesses:
        game.guess(letter)
        if game.status == "playing":
            assert "cat" not in str(game.to_dict())
            assert "cat" not in repr(game)
    assert game.status == outcome
    assert game.to_dict()["word"] == "cat"
    assert game.remaining_guesses == (6 if outcome == "won" else 0)
    before = game.to_dict()
    with pytest.raises(GameOverError):
        game.guess("z")
    assert game.to_dict() == before
    with pytest.raises(GameOverError):
        game.guess(guesses[0].upper())
    assert game.to_dict() == before
    with pytest.raises(InvalidGuessError):
        game.guess("ab")
    assert game.to_dict() == before


def test_errors_share_common_base():
    assert all(issubclass(error, GameError) for error in (InvalidGuessError, GameOverError, DuplicateGuessError))
    assert issubclass(GameError, ValueError)
