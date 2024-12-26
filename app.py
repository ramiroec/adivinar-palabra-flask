from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'secret_key'

def get_random_word():
    words = ["python", "programacion", "desarrollador", "codigo", "computadora"]
    return random.choice(words)

def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

@app.route('/')
def index():
    session['word'] = get_random_word()
    session['guessed_letters'] = []
    session['attempts'] = 6
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'word' not in session:
        return redirect(url_for('index'))

    word = session['word']
    guessed_letters = session['guessed_letters']
    attempts = session['attempts']

    message = ""
    
    if request.method == 'POST':
        guess = request.form.get('guess', '').lower()

        if not guess.isalpha() or len(guess) != 1:
            message = "Por favor, ingresa una sola letra."
        elif guess in guessed_letters:
            message = "Ya has adivinado esa letra."
        else:
            guessed_letters.append(guess)
            if guess in word:
                message = "¡Buena elección!"
            else:
                attempts -= 1
                session['attempts'] = attempts
                message = f"Letra incorrecta. Te quedan {attempts} intentos."

    display = display_word(word, guessed_letters)

    if '_' not in display:
        return render_template('win.html', word=word)

    if attempts == 0:
        return render_template('lose.html', word=word)

    session['guessed_letters'] = guessed_letters

    return render_template('game.html', display=display, attempts=attempts, message=message, guessed_letters=guessed_letters)

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
