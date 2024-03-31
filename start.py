from flask import Flask, render_template, request, session
from MemoryGame import MemoryGame
from GuessGame import GuessGame
from CurrencyRouletteGame import CurrencyRouletteGame
from Scores import add_score, SCORES_FILE_NAME
import random
import os


app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'fallback_secret_key')

try:
    with open(SCORES_FILE_NAME, 'r') as score_file:
        current_score = int(score_file.read())
except (FileNotFoundError, ValueError):
    current_score = 0


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/memory-game', methods=['GET', 'POST'])
def memory_game():

    if request.method == 'GET':
        player_name = request.args.get('name', 'Player')
        difficulty_level = request.args.get('difficulty', default=1, type=int)
        session['name'] = player_name
        session['difficulty'] = difficulty_level

    if request.method == 'POST':
        player_name = session.get('name', 'Player')
        difficulty_level = request.args.get('difficulty', default=1, type=int)
        user_sequence = [int(num) for num in request.form.get('userSequence', '').split()]
        correct_sequence = session.get('sequence', [])
        game = MemoryGame(difficulty_level)
        won = game.play(correct_sequence, user_sequence)
        if won:
            new_score = add_score(current_score, difficulty_level)
        else:
            new_score = current_score

        message = game.end_game(won)
        return render_template('gameResult.html', message=message, sequence=correct_sequence,
                               name=player_name, score=new_score)

    game = MemoryGame(session.get('difficulty', 1))
    sequence = game.generate_sequence()
    session['sequence'] = sequence

    return render_template('memoryGame.html', name=player_name, difficulty=difficulty_level, sequence=sequence)


@app.route('/guess-game', methods=['GET', 'POST'])
def guess_game():
    player_name = request.args.get('name', 'Player')
    difficulty_level = request.args.get('difficulty', default=1, type=int)
    game = GuessGame(difficulty_level)
    if request.method == 'POST':
        guess = int(request.form.get('guess', 0))
        won, secret_number = game.play(guess)
        if won:
            new_score = add_score(current_score, difficulty_level)
        else:
            new_score = current_score

        message = game.end_game(won)
        return render_template('gameResult.html', message=message, name=player_name,
                               score=new_score, secret_number=secret_number)

    return render_template('guessGame.html', name=player_name, difficulty=difficulty_level)


@app.route('/currency-roulette-game', methods=['GET', 'POST'])
def currency_roulette_game():
    player_name = session.get('name', 'Player')
    difficulty_level = request.args.get('difficulty', default=1, type=int)

    if request.method == 'POST':
        guess = float(request.form.get('guess', 0))
        amount_in_usd = session.get('amount_in_usd')
        game = CurrencyRouletteGame(difficulty_level)
        won, interval = game.play(guess, amount_in_usd)
        if won:
            new_score = add_score(current_score, difficulty_level)
        else:
            new_score = current_score

        session.pop('amount_in_usd', None)
        message = game.end_game(won)
        return render_template('gameResult.html', message=message, name=player_name,
                               score=new_score, interval=interval)
    else:
        amount_in_usd = random.randint(1, 100)
        session['amount_in_usd'] = amount_in_usd

    return render_template('currencyRouletteGame.html', name=player_name,
                           difficulty=difficulty_level, amount_in_usd=amount_in_usd)


@app.route('/score')
def score_page():
    return f'<h1>Current Score:</h1><p id="current_score">{current_score}</p>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8777)
