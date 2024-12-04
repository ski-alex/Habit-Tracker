from datetime import datetime, timedelta
from tabulate import tabulate
import questionary

import manage
from manage import Habit


def display_habits(habits, status_request, length):
    if Habit.check_habits_exist(habits):
        return
    
    header_short = ["ID", "Name", "Category", "Period", "Target", "Streak", "Last Checked", "Deadline", "Status"]
    header_full = ["ID", "Name", "Category", "Period", "Target", "Streak", "Max Streak", "Created On", "Last Checked", "Deadline", "Status", "Interruptions"]
            
    if length == "full":
        header = header_full
    else:
        header = header_short

    table_data = []

    for habit in habits:
        latest_check_date = max(habit.date_check, default="N/A")
        no_interruptions = len(habit.interruptions)
        period_word = {1: "Daily", 2: "Every two days", 7: "Weekly"}[habit.period]

        if habit.status != status_request:
            if length == "full":
                row = [habit.id_h, habit.name, habit.category, period_word, habit.target, habit.streak, habit.streak_max, habit.date_create, latest_check_date, habit.deadline, habit.status, no_interruptions]
            else:
                row = [habit.id_h, habit.name, habit.category, period_word, habit.target, habit.streak, latest_check_date, habit.deadline, habit.status]
         
            table_data.append(row)

    print(tabulate(table_data, headers=header, tablefmt="github"))

## FILTER
def filter_indiv(habits):
    if Habit.check_habits_exist(habits):
        return
    
    attribute = questionary.select("Which attribute do you want to filter?",choices=["ID", "Name", "Category", "Period"]).ask().lower()
    
    if attribute == "id":
        attribute = "id_h"  # adjust, since "id" is not the real attribute name
        comp_word = questionary.select("For what do you want to filter?",choices=["exact value", "greater values", "smaller values"]).ask() 
        comp_symbol = {"exact value": "=", "greater values": ">", "smaller values": "<"}[comp_word] 
        try:
            value = int(questionary.text(f"The values should be {comp_word}").ask())
        except ValueError:
            print("Invalid input. Please enter a positve integer.")
            return None
        
    elif attribute == "name":
        value = questionary.text("What should the attribute name contain?").ask().lower()

    elif attribute == "category":
        value = questionary.checkbox("Select at least one category you want to filter for:",choices=manage.categories).ask()
        print(f"You have chosen {' and '.join(value)}")

    elif attribute == "period": 
        period_words = questionary.checkbox("Select at least one period you want to filter for:",choices=manage.periods).ask() 
        print(f"You have chosen {' and '.join(period_words)}") 
        period_mapping = {"Daily": 1, "Every two days": 2, "Weekly": 7} 
        value = [period_mapping[p] for p in period_words]
    

    header = ["ID", "Name", "Category", "Period", "Target", "Streak", "Max Streak", "Created On", "Last Checked", "Deadline", "Status", "Interruptions"]
    table_data = []
    
    for habit in habits:
  
        match = False
        if attribute == "id_h":
            if comp_symbol == "=":
                match = getattr(habit, attribute) == value 
            elif comp_symbol == ">":
                match = getattr(habit, attribute) > value 
            elif comp_symbol == "<":
                match = getattr(habit, attribute) < value

        elif attribute == "name":
            if value in str(getattr(habit, attribute)).lower():
                match = True

        elif attribute == "category":
            if getattr(habit, attribute).lower() in [v.lower() for v in value]:
                match = True

        elif attribute == "period": 
            if getattr(habit, attribute) in value:
                match = True

        if match: 
            latest_check_date = max(habit.date_check, default="N/A")
            no_interruptions = len(habit.interruptions)
            period_word = {1:"Daily", 2:"Every two days", 7:"Weekly"}[habit.period]

            row = [habit.id_h, habit.name, habit.category, period_word, habit.target, habit.streak, habit.streak_max, habit.date_create, latest_check_date, habit.deadline, habit.status, no_interruptions]
            table_data.append(row)
    
    print(tabulate(table_data, headers=header, tablefmt="github"))