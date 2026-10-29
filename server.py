"""Flask API and static asset entry point."""

import os
from uuid import uuid4

from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException, NotFound, UnsupportedMediaType

from game import DuplicateGuessError, GameOverError, HangmanGame, InvalidGuessError
from word_manager import WordManager


def create_app(word_manager=None):
    app = Flask(__name__)
    app.config["WORD_MANAGER"] = word_manager if word_manager is not None else WordManager()
    app.extensions["games"] = {}

    def body_with_field(field):
        if not request.is_json:
            raise UnsupportedMediaType("A JSON content type is required")
        body = request.get_json()
        if not isinstance(body, dict) or set(body) != {field} or not isinstance(body[field], str):
            raise BadRequest(f"Expected a JSON object with a single string field: {field}")
        return body[field]

    @app.errorhandler(Exception)
    def handle_error(error):
        if isinstance(error, HTTPException):
            response = error.get_response()
            response.set_data(jsonify(error=error.description).get_data())
            response.content_type = "application/json"
            return response
        app.logger.exception("Unhandled request error")
        return jsonify(error="Internal server error"), 500

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.post("/api/games")
    def create_game():
        difficulty = body_with_field("difficulty")
        try:
            word = app.config["WORD_MANAGER"].get_random_word(difficulty)
        except ValueError as error:
            raise BadRequest(str(error)) from error
        game_id = uuid4().hex
        game = HangmanGame(word, difficulty, game_id)
        app.extensions["games"][game_id] = game
        return jsonify(game.to_dict()), 201

    def find_game(game_id):
        game = app.extensions["games"].get(game_id)
        if game is None:
            raise NotFound("Game not found")
        return game

    @app.get("/api/games/<game_id>")
    def get_game(game_id):
        return jsonify(find_game(game_id).to_dict())

    @app.post("/api/games/<game_id>/guess")
    def guess(game_id):
        game = find_game(game_id)
        letter = body_with_field("letter")
        try:
            game.guess(letter)
        except (InvalidGuessError, DuplicateGuessError) as error:
            return jsonify(error=str(error)), 400
        except GameOverError as error:
            return jsonify(error=str(error)), 409
        return jsonify(game.to_dict())

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
