import datetime
import json
import os
import google.generativeai as genai
from plyer import notification

# ⛓️ Setup Gemini
GEMINI_API_KEY = "AIzaSyC4ooZ-Gc9qbVDZmhVfsss9j_4mEG0zIq0"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

DATA_FILE = "habit_tracker.json"

# 📁 Load or create habit log
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_habit_data(json_path="habit_tracker.json"):
    try:
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Habit JSON file not found.")
        return {}
    except json.JSONDecodeError:
        print("❌ Error parsing JSON file.")
        return {}

# ✅ Log today's habits
def log_habits(habits_done):
    today = str(datetime.date.today())
    data = load_data()
    data[today] = habits_done
    save_data(data)
    print(f"\n📥 Saved today's habits.")
    return data

# 🤖 Ask Gemini for suggestions
def get_ai_suggestions(habit_history):
    prompt = f"""
You are an AI wellness coach. List all the habits logged by the user for today.
Sort the habits in ascending order of time.
Display each habit with a checkbox to mark it as completed.
Format neatly and concisely. 

Habit log:\n{json.dumps(habit_history, indent=2)}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def get_ai_suggestions1(habit_history):
    prompt = f"""
You are an AI wellness coach. Based on the habits logged today, suggest 3 new healthy habits for tomorrow.
Be encouraging, specific, and focus on replacements or balance.
Format as a numbered list with short titles and explanations.

Habit log:\n{json.dumps(habit_history, indent=2)}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

def get_ai_suggestions2(habit_history):
    prompt = f"""
You are an AI wellness coach. Write a positive and empathetic performance summary for the user based on today’s habits.
Emphasize their awareness and effort, encourage persistence, and inspire consistency in habit tracking. keep it short and have only one heading Your Performance Today:

Habit log:\n{json.dumps(habit_history, indent=2)}
"""
    response = model.generate_content(prompt)
    return response.text.strip()


# 🔔 Reminder
def send_reminder():

    notification.notify(
        title="🌟 Habit Reminder",
        message="Don't forget to log your habits today!",
        timeout=5
    )

# 🚀 Main Flow
def main():
    send_reminder()

    print(" Welcome to the AI Habit Tracker!\n")

    habits = load_habit_data()
    habits_done = [h.strip() for h in habits if h.strip()]
    
    if not habits_done:
        print("⚠️ No habits entered. Try again.")
        return

    history = log_habits(habits_done)
    
    print("\n🤖 Getting AI suggestions based on your progress...\n")
    feedback = get_ai_suggestions(history)
    print(feedback)
    feedback1 = get_ai_suggestions1(history)
    print(feedback1)
    feedback2 = get_ai_suggestions2(history)
    print(feedback2)

if __name__ == "__main__":
    main()
