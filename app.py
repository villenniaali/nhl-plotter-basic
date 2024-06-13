from flask import Flask, redirect, url_for, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot_game():
    game_id = request.form['game_id']
    # Call the shots.py script with the game_id
    subprocess.run(['python', 'shots.py', game_id])
    # Redirect to the endpoint that displays the saved plot
    return redirect(url_for('display_plot', game_id=game_id))

@app.route('/plot/display/<int:game_id>')
def display_plot(game_id):
    # Render the template to display the saved plot
    return render_template('plot.html', game_id=game_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
