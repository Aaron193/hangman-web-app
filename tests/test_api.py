import pytest

from server import create_app
from word_manager import WordManager


WORDS = {"easy": "qux", "medium": "zephyr", "hard": "blackjumpy"}


@pytest.fixture
def manager(tmp_path):
    for difficulty, word in WORDS.items():
        (tmp_path / f"{difficulty}.txt").write_text(word + "\n")
    return WordManager(tmp_path)


@pytest.fixture
def client(manager):
    return create_app(manager).test_client()


def create(client, difficulty="hard"):
    response = client.post("/api/games", json={"difficulty": difficulty})
    assert response.status_code == 201
    return response.get_json()


def guess(client, game_id, letter):
    return client.post(f"/api/games/{game_id}/guess", json={"letter": letter})


def assert_error(response, status):
    assert response.status_code == status
    assert response.is_json
    assert set(response.get_json()) == {"error"}
    assert isinstance(response.get_json()["error"], str)


@pytest.mark.parametrize("difficulty", WORDS)
def test_creation_and_retrieval(client, difficulty):
    state = create(client, difficulty)
    assert state == {"game_id": state["game_id"], "difficulty": difficulty,
                     "pattern": " ".join("_" * len(WORDS[difficulty])),
                     "guessed_letters": [], "incorrect_letters": [],
                     "remaining_guesses": 6, "status": "playing"}
    response = client.get(f"/api/games/{state['game_id']}")
    assert response.status_code == 200
    assert response.get_json() == state
    assert WORDS[difficulty] not in response.get_data(as_text=True)


def test_independent_games_and_app_stores(client, manager):
    first, second = create(client), create(client)
    assert first["game_id"] != second["game_id"]
    guess(client, first["game_id"], "b")
    assert client.get(f"/api/games/{second['game_id']}").get_json() == second
    other = create_app(manager).test_client()
    assert_error(other.get(f"/api/games/{first['game_id']}"), 404)


@pytest.mark.parametrize("payload,status", [
    ({"data": "{}", "content_type": "text/plain"}, 415),
    ({"data": "{", "content_type": "application/json"}, 400),
    ({"json": []}, 400), ({"json": None, "content_type": "application/json"}, 400),
    ({"json": {}}, 400), ({"json": {"difficulty": 1}}, 400),
    ({"json": {"difficulty": "easy", "extra": 1}}, 400),
    ({"json": {"difficulty": "unknown"}}, 400),
])
def test_create_bad_requests(client, payload, status):
    assert_error(client.post("/api/games", **payload), status)


@pytest.mark.parametrize("payload,status", [
    ({"data": "{}", "content_type": "text/plain"}, 415),
    ({"data": "{", "content_type": "application/json"}, 400),
    ({"json": []}, 400), ({"json": {}}, 400),
    ({"json": {"letter": 1}}, 400),
    ({"json": {"letter": "a", "extra": 1}}, 400),
])
def test_guess_bad_requests(client, payload, status):
    game_id = create(client)["game_id"]
    assert_error(client.post(f"/api/games/{game_id}/guess", **payload), status)
    assert_error(client.post("/api/games/missing/guess", **payload), 404)


def test_unknown_id_methods_and_routes(client):
    assert_error(client.get("/api/games/missing"), 404)
    response = client.get("/api/games")
    assert_error(response, 405)
    assert "POST" in response.headers["Allow"].split(", ")
    assert_error(client.get("/unknown"), 404)


@pytest.mark.parametrize("letter", ["", "ab", "1", "é", " "])
def test_invalid_and_duplicate_guesses_preserve_state(client, letter):
    state = create(client)
    game_id = state["game_id"]
    assert_error(guess(client, game_id, letter), 400)
    assert client.get(f"/api/games/{game_id}").get_json() == state
    accepted = guess(client, game_id, "B").get_json()
    assert_error(guess(client, game_id, "b"), 400)
    assert client.get(f"/api/games/{game_id}").get_json() == accepted


@pytest.mark.parametrize("letters,outcome", [("blackjumpy", "won"), ("defghi", "lost")])
def test_complete_games_and_secrecy(client, letters, outcome):
    response = client.post("/api/games", json={"difficulty": "hard"})
    state = response.get_json()
    game_id = state["game_id"]
    assert WORDS["hard"] not in response.get_data(as_text=True)
    for letter in letters:
        response = guess(client, game_id, letter)
        assert response.status_code == 200
        state = response.get_json()
        retrieved = client.get(f"/api/games/{game_id}")
        assert retrieved.get_json() == state
        if state["status"] == "playing":
            assert WORDS["hard"] not in response.get_data(as_text=True)
            assert WORDS["hard"] not in retrieved.get_data(as_text=True)
    assert state["status"] == outcome
    assert state["word"] == WORDS["hard"]
    assert WORDS["hard"] in response.get_data(as_text=True)
    assert_error(guess(client, game_id, "z"), 409)
    assert client.get(f"/api/games/{game_id}").get_json() == state


def test_static_assets(client):
    assert client.get("/").status_code == 200
    assert client.get("/static/app.js").status_code == 200


def test_unexpected_errors_are_json(manager):
    app = create_app(manager)

    @app.get("/failure")
    def failure():
        raise RuntimeError("private details")

    response = app.test_client().get("/failure")
    assert_error(response, 500)
    assert "private details" not in response.get_data(as_text=True)
