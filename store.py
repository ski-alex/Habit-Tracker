import json
from manage import Habit 

class HabitsStore():
    DEFAULT_FILENAME = "habits.json"
    
    def save(self, habits, filename = DEFAULT_FILENAME):
        with open(filename, 'w') as file:
            json.dump([habit.__dict__ for habit in habits], file, indent=4)
        print(f"Habits saved in {filename} .")

    def load(self, filename = DEFAULT_FILENAME):
        try:
            with open(filename, 'r') as file:
                habits_data = json.load(file) 
                return [Habit(**habit) for habit in habits_data]
        except FileNotFoundError:
            return []