import json
import os
import platform
import subprocess

DATA_FILE = 'habit_tracker.json'

# Load stored data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Prompt user for a habit
def get_habit_input(habit_type):
    print(f"\nEnter a {habit_type} habit:")
    name = input("Habit Name: ")
    time = input("Preferred Time (e.g., 7:00 AM): ")
    return {"name": name, "frequency": habit_type.lower(), "time": time}

# Display all saved habits
def display_habits(habits):
    print("\n=== Your Habit Summary ===")
    for habit in habits:
        print(f"- [{habit['frequency'].capitalize()}] {habit['name']} at {habit['time']}")
    print("===========================")

# Open file location in file explorer
def open_file_location(filepath):
    try:
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(filepath))
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", os.path.abspath(filepath)])
        else:  # Linux
            subprocess.call(["xdg-open", os.path.abspath(filepath)])
    except Exception as e:
        print(f"⚠ Unable to open file location: {e}")

# Main logic
if __name__ == "__main__":
    user_id = input("Enter your username: ").strip()
    user_data = load_data()

    
    
    choice = "1"

    habit_type_map = {"1": "Daily", "2": "Weekly", "3": "Monthly"}
    habit_type = habit_type_map.get(choice)

    if not habit_type:
        print("❌ Invalid choice. Please run the program again and select 1, 2, or 3.")
        exit()

    habits = []
    while True:
        habit = get_habit_input(habit_type)
        habits.append(habit)

        more = input("Add another habit? (yes/no): ").strip().lower()
        if more != 'yes':
            break

    # Save data under user_id
    if user_id in user_data:
        user_data[user_id].extend(habits)
    else:
        user_data[user_id] = habits

    save_data(user_data)

    # Show result
    display_habits(user_data[user_id])
    print(f"\n✅ Habits saved to '{DATA_FILE}' under user: {user_id}")
    print("📄 Final Data:")
    print(json.dumps(user_data[user_id], indent=4))

    # Open file location
    print("\n📂 Opening file location...")
    open_file_location(DATA_FILE)
