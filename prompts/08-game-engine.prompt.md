phase 3 now, the game engine in game.py. it has to stay independent of flask. here's the shape I want so the server stays thin later:

- a HangmanGame class built from the word, the difficulty and a game id (it can just hold on to the id and difficulty so it can serialize itself). validate the word (non-empty, a-z only), lowercase it, and allow six incorrect guesses.
- guess(letter) returns True if the letter is in the word and False if not. it should raise our own exceptions, all subclassing a common GameError(ValueError): InvalidGuessError (not a string, or not exactly one ascii letter, so digits, symbols, spaces, "ab", "é" and so on), GameOverError (guess after a win or loss) and DuplicateGuessError (same letter again, case-insensitive). check them in that order: invalid first, then game over, then duplicate. none of them may change the game or cost a guess. uppercase input just gets lowercased.
- the usual state: status (playing / won / lost), pattern as space-separated letters and underscores (watch repeated letters, like banana), guessed_letters and incorrect_letters in guess order, and remaining_guesses.
- to_dict() should return exactly the game JSON from the decisions section in the TODO. the word only shows up once the game is won or lost, and nothing else that gives away the answer while it's still being played. repr() shouldn't print the word either.

tests/test_game.py: deterministic tests with fixed words covering correct and incorrect guesses, repeated guesses (no state change, no life lost), every kind of invalid input, uppercase, wins, losses, repeated letters in the pattern, guesses after a win and after a loss (state unchanged), the error precedence, and the word never showing up in to_dict() or repr() while playing but showing up after a win and after a loss.

run all the tests, tick what you verified in the TODO, no commits.
