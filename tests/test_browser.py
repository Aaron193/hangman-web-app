"""Exercise the real client and server in an installed Chrome browser."""

import os
import re
import shutil
import threading

import pytest
from werkzeug.serving import make_server

playwright = pytest.importorskip("playwright.sync_api", reason="Playwright is not installed")
from server import create_app
from word_manager import WordManager

CHROME = os.environ.get("CHROME_PATH") or shutil.which("google-chrome")
if not CHROME or not os.path.isfile(CHROME) or not os.access(CHROME, os.X_OK):
    pytest.skip("Chrome executable unavailable (set CHROME_PATH)", allow_module_level=True)


@pytest.fixture
def server_url(tmp_path):
    for level, word in {"easy": "cat", "medium": "rabbit", "hard": "butterfly"}.items():
        (tmp_path / f"{level}.txt").write_text(word + "\n")
    server = make_server("127.0.0.1", 0, create_app(WordManager(tmp_path)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join()
    server.server_close()


@pytest.fixture
def page():
    with playwright.sync_playwright() as p:
        try:
            browser = p.chromium.launch(executable_path=CHROME, headless=True)
        except playwright.Error as exc:
            pytest.skip(f"Chrome could not launch: {exc}")
        page = browser.new_page()
        yield page
        browser.close()


def start(page, server_url):
    page.goto(server_url)
    playwright.expect(page.locator("#remaining")).to_have_text("6")


def guess(page, letter):
    page.locator(f'[data-letter="{letter}"]').click()
    button = page.locator(f'[data-letter="{letter}"]')
    playwright.expect(button).to_have_attribute("aria-label", re.compile(r", (correct|wrong)$"))
    playwright.expect(button).to_be_disabled()


def displays(page):
    return page.locator(".parts > *").evaluate_all(
        "parts => parts.map(part => getComputedStyle(part).display !== 'none')"
    )


def test_initial_and_guesses(page, server_url):
    start(page, server_url)
    playwright.expect(page.locator("#difficulty")).to_have_value("medium")
    playwright.expect(page.locator("#pattern")).to_have_text("_ _ _ _ _ _")
    assert displays(page) == [False] * 6
    guess(page, "b")
    playwright.expect(page.locator("#pattern")).to_have_text("_ _ b b _ _")
    playwright.expect(page.locator('[data-letter="b"]')).to_have_attribute("aria-label", "B, correct")
    assert displays(page) == [False] * 6
    for count, letter in enumerate("cdefgh", 1):
        guess(page, letter)
        playwright.expect(page.locator("#remaining")).to_have_text(str(6 - count))
        playwright.expect(page.locator(f'[data-letter="{letter}"]')).to_have_attribute("aria-label", f"{letter.upper()}, wrong")
        assert displays(page) == [True] * count + [False] * (6 - count)
    playwright.expect(page.locator("#status")).to_have_text("You lost. The word was rabbit.")
    assert page.locator("#keyboard button:disabled").count() == 26


def test_win_and_reset(page, server_url):
    start(page, server_url)
    for letter in "rabit":
        guess(page, letter)
    playwright.expect(page.locator("#status")).to_have_text("You won! The word was rabbit.")
    assert page.locator("#keyboard button:disabled").count() == 26
    playwright.expect(page.locator("#new-game")).to_be_focused()
    page.locator("#new-game").click()
    playwright.expect(page.locator("#pattern")).to_have_text("_ _ _ _ _ _")
    playwright.expect(page.locator("#status")).to_have_text("")
    playwright.expect(page.locator("#remaining")).to_have_text("6")
    playwright.expect(page.locator("#guessed")).to_have_text("None yet")
    playwright.expect(page.locator("#incorrect")).to_have_text("None yet")
    assert page.locator("#keyboard button:disabled").count() == 0
    assert displays(page) == [False] * 6


@pytest.mark.parametrize("level,letter,pattern", [
    ("easy", "c", "c _ _"), ("medium", "r", "r _ _ _ _ _"),
    ("hard", "y", "_ _ _ _ _ _ _ _ y"),
])
def test_difficulties(page, server_url, level, letter, pattern):
    start(page, server_url)
    page.locator("#difficulty").select_option(level)
    page.locator("#new-game").click()
    playwright.expect(page.locator("#pattern")).to_have_text(" ".join("_" * len(pattern.split())))
    guess(page, letter)
    playwright.expect(page.locator("#pattern")).to_have_text(pattern)


def test_physical_keyboard(page, server_url):
    start(page, server_url)
    page.keyboard.press("Control+c")
    playwright.expect(page.locator("#guessed")).to_have_text("None yet")
    page.keyboard.press("B")
    playwright.expect(page.locator("#pattern")).to_have_text("_ _ b b _ _")
    playwright.expect(page.locator("#guessed")).to_have_text("B")
    playwright.expect(page.locator('[data-letter="b"]')).to_be_disabled()


@pytest.mark.parametrize("failure,message", [
    ("404", "This game is gone. Start a new game to play again."),
    ("network", "Network error. Please check your connection and try again."),
])
def test_request_errors(page, server_url, failure, message):
    start(page, server_url)
    def fail(route):
        if failure == "404":
            route.fulfill(status=404, content_type="application/json", body='{"error":"Game not found"}')
        else:
            route.abort("failed")
    page.route("**/api/games/*/guess", fail)
    page.locator('[data-letter="c"]').click()
    playwright.expect(page.locator("#status")).to_have_text(message)
    if failure == "404":
        assert page.locator("#keyboard button:disabled").count() == 26
    else:
        playwright.expect(page.locator('[data-letter="c"]')).to_be_enabled()


def test_api_responses_hide_word_and_guess_shape(page, server_url):
    responses = []
    page.on("response", lambda response: responses.append(response) if "/api/games" in response.url else None)
    start(page, server_url)
    guess(page, "b")
    guess(page, "c")
    assert len(responses) == 3
    for response in responses:
        data = response.json()
        assert data["status"] == "playing"
        assert "word" not in data
        assert "rabbit" not in response.text().lower()
    response = responses[1]
    assert response.request.method == "POST"
    assert response.request.post_data_json == {"letter": "b"}
    assert response.status == 200
    assert set(response.json()) == {"game_id", "difficulty", "pattern", "guessed_letters", "incorrect_letters", "remaining_guesses", "status"}
