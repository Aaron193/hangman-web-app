from pathlib import Path
import random
import re

import pytest

from word_manager import WordManager


@pytest.fixture
def words_dir(tmp_path):
    for difficulty, contents in {
        "easy": "cat\ndog\n",
        "medium": "rabbit\nforest\n",
        "hard": "butterfly\nstrawberry\n",
    }.items():
        (tmp_path / f"{difficulty}.txt").write_text(contents, encoding="utf-8")
    return tmp_path


@pytest.mark.parametrize("difficulty", WordManager.DIFFICULTIES)
def test_selects_from_the_correct_list(words_dir, difficulty):
    manager = WordManager(words_dir, random.Random(42))
    expected = set((words_dir / f"{difficulty}.txt").read_text().splitlines())
    assert all(manager.get_random_word(difficulty) in expected for _ in range(20))
    first = WordManager(words_dir, random.Random(42))
    second = WordManager(words_dir, random.Random(42))
    assert [first.get_random_word(difficulty) for _ in range(20)] == [
        second.get_random_word(difficulty) for _ in range(20)
    ]


@pytest.mark.parametrize("difficulty", ["Easy", " easy", "", "unknown", None, 1, [], {}])
def test_invalid_difficulty(words_dir, difficulty):
    with pytest.raises(ValueError, match="Invalid difficulty"):
        WordManager(words_dir).get_random_word(difficulty)


@pytest.mark.parametrize("entry", ["bad-word", "word2", "café", "two words"])
def test_invalid_entry_names_file_and_entry(words_dir, entry):
    path = words_dir / "medium.txt"
    path.write_text(f"valid\n{entry}\n", encoding="utf-8")
    with pytest.raises(ValueError) as error:
        WordManager(words_dir)
    assert str(path) in str(error.value)
    assert entry in str(error.value)


def test_empty_list_names_file(words_dir):
    path = words_dir / "easy.txt"
    path.write_text("  \n\t\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty") as error:
        WordManager(words_dir)
    assert str(path) in str(error.value)


def test_missing_list_names_file(words_dir):
    path = words_dir / "hard.txt"
    path.unlink()
    with pytest.raises(ValueError, match="not found") as error:
        WordManager(words_dir)
    assert str(path) in str(error.value)


def test_normalizes_and_deduplicates(words_dir):
    (words_dir / "easy.txt").write_text(" Cat \ncat\n\n DOG\n dog \n", encoding="utf-8")
    assert WordManager(words_dir).words["easy"] == ["cat", "dog"]


@pytest.mark.parametrize("difficulty,minimum,maximum", [("easy", 3, 5), ("medium", 6, 8), ("hard", 9, None)])
def test_real_word_lists(difficulty, minimum, maximum, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    manager = WordManager(rng=random.Random(1))
    path = Path(__file__).resolve().parents[1] / "words" / f"{difficulty}.txt"
    entries = path.read_text(encoding="utf-8").splitlines()
    assert len(entries) >= 50
    assert len(entries) == len(set(entries))
    assert all(re.fullmatch(r"[a-z]+", word) for word in entries)
    assert all(len(word) >= minimum and (maximum is None or len(word) <= maximum) for word in entries)
    assert manager.words[difficulty] == entries
    assert manager.get_random_word(difficulty) in entries
