from datetime import datetime
from tabulate import tabulate
from manage import Habit
import manage

class Analyse:
    @classmethod
    def get_top_main(cls, habits, attribute, attribute_name, attribute_descriptions):
        sorted_habits = sorted(habits, key=lambda habit: getattr(habit, attribute), reverse=True)
        top_3_habits = sorted_habits[:3]
   
        table_data = []
        for habit in top_3_habits:
            if getattr(habit, attribute) > 0:
                table_data.append([habit.id_h, habit.name, getattr(habit, attribute)])
        if not table_data:
            print("No results found for this filter.")
        else:
            print(f"Here are the habits with the {attribute_descriptions}:")
            print(tabulate(table_data, headers=["ID", "Name", attribute_name], tablefmt="github"))

    @classmethod
    def get_top_most_interruptions(cls, habits):
        sorted_habits = sorted(habits, key=lambda habit: len(habit.interruptions), reverse=True)
        top_3_habits = sorted_habits[:3]

        table_data = []
        for habit in top_3_habits:
            if len(habit.interruptions) > 0:
                table_data.append([habit.id_h, habit.name, len(habit.interruptions)])
        if not table_data:
            print("No results found for this filter.")
        else:
            print("Here are the habits with the most interruptions:")
            print(tabulate(table_data, headers=["ID", "Name", "Interruptions"], tablefmt="github"))

    @classmethod
    def get_top_longestExpired(cls, habits):
        now = datetime.now().strftime("%Y-%m-%d")

        sorted_habits = sorted(habits, key=lambda habit: habit.deadline, reverse=False)
        top_3_habits = sorted_habits[:3]

        table_data = []
        for habit in top_3_habits:
            if habit.deadline < now:
                table_data.append([habit.id_h, habit.name, habit.deadline])
        if not table_data:
            print("No results found for this filter.")
        else:
            print("Here are the habits that have not been worked on for the longest time:")
            print(tabulate(table_data, headers=["ID", "Name", "Deadline"], tablefmt="github"))

    @classmethod
    def get_group_habitsByCategory(cls, habits):
        all_categories = manage.categories

        category_count = {category: {'total': 0, 'active': 0, 'broken': 0, 'established': 0} for category in all_categories}

        for habit in habits:
            if habit.category in category_count:
                category_count[habit.category]['total'] += 1
                if habit.status == "Active":
                    category_count[habit.category]['active'] += 1
                elif habit.status == "Broken":
                    category_count[habit.category]['broken'] += 1
                elif habit.status == "Established":
                    category_count[habit.category]['established'] += 1

        table_data = []
        for category, counts in category_count.items():
            table_data.append([category, counts['total'], counts['active'], counts['broken'], counts['established']])
        if not table_data:
            print("No results found for this filter.")
        else:
            print("Here is a grouping of all habits by category:")
            print(tabulate(table_data, headers=["Category", "Total", "Active", "Broken", "Established"], tablefmt="github"))

    @classmethod
    def get_all_main(cls, habits, status, status_name):
        table_data = []
        for habit in habits:
            if habit.status == status:
                table_data.append([habit.id_h, habit.name, habit.status])
        if not table_data:
            print("No results found for this filter.")
        else:
            print(f"Here are all {status_name} habits:")
            print(tabulate(table_data, headers=["ID", "Name", "Status"], tablefmt="github"))