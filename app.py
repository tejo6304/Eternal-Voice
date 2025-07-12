from flask import Flask, render_template, request, redirect, url_for, session 
import json
import os
from HabittrackerAI import get_ai_suggestions, get_ai_suggestions1, get_ai_suggestions2

app = Flask(__name__)
app.secret_key = 'trackersecret'

DATA_FILE = 'habit_tracker.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['user_id'] = request.form['user_id'].strip()
        return redirect(url_for('enter_habit'))
    return render_template('index.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter_habit():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']
    user_data = load_data()
    user_history = user_data.get(user_id, [])

    if request.method == 'POST':
        habit_name = request.form['habit']
        time = request.form['time']
        new_habit = {"name": habit_name, "frequency": "daily", "time": time}

        if user_id in user_data:
            user_data[user_id].append(new_habit)
        else:
            user_data[user_id] = [new_habit]

        save_data(user_data)

        if 'add_more' in request.form:
            return redirect(url_for('enter_habit'))
        else:
            return redirect(url_for('index'))
    
    feedback = get_ai_suggestions(user_history)
    feedback1 = get_ai_suggestions1(user_history)
    feedback2 = get_ai_suggestions2(user_history)



    return render_template(
    'AIcoach.html',
    user_id=user_id,
    feedback=feedback,
    feedback1=feedback1,
    feedback2=feedback2)

if __name__ == '__main__':
    app.run(debug=True)
