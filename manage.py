from datetime import datetime, timedelta
import questionary

categories = ["Health", "Lifestyle", "Sport", "Education", "Else"]
periods = ["Daily", "Every two days", "Weekly"]

class Habit:
    def __init__(self, id_h, name, category, period, target, streak=0, streak_max=0, date_create=None, date_check=None, deadline=None, status="Active", interruptions=None): 
        self.id_h = id_h 
        self.name = name 
        self.category = category 
        self.period = int(period) 
        self.target = target 
        self.streak = streak 
        self.streak_max = streak_max 
        self.date_create = date_create or datetime.now().strftime("%Y-%m-%d") 
        self.date_check = date_check or [] 
        self.deadline = deadline or (datetime.now() + timedelta(days=period)).strftime("%Y-%m-%d") 
        self.status = status 
        self.interruptions = interruptions or []

# ADD new habit
    @classmethod
    def add(cls, habits):
        id_h = cls.get_id(habits)
        name = questionary.text("Please enter the name of your new habit:").ask()
        category = cls.enter_category()
        period = cls.enter_period()
        target = cls.enter_valid_target()

        new_habit = cls(id_h, name, category, int(period), target) 

        period_word = {1:"Daily", 2:"Every two days", 7:"Weekly"}[period].lower()
        confirmation = questionary.confirm(f"Do you want to add '{name}' in {category} and repeat it {period_word} for {target} times?").ask() 
        if confirmation:
            habits.append(new_habit) 
            print(f"'{name}' successfully added.")

# ADJUST habit
    @classmethod
    def adjust(cls, habits):
        if cls.check_habits_exist(habits):
            return
        
        habit_id = cls.check_id_exists(habits, occasion_name="adjust")
        if habit_id is None:
            return

        habit_to_adjust = next((habit for habit in habits if habit.id_h == habit_id), None)
        
        if habit_to_adjust.status == "Established":
            print("This habit is already established. If you want to re-establish this habit, you can use the “Duplicate” function.")
            return
        
        choice = questionary.select(
            "Which attribute do you want to adjust?",
            choices=["Name", "Category", "Period", "Target"]
        ).ask().lower()

        habit_to_adjust = next((habit for habit in habits if habit.id_h == habit_id), None)

        if choice == "name":
            new_value = questionary.text("Please enter the new name of your habit:").ask()
        elif choice == "category":
            new_value = cls.enter_category()
        elif choice == "period":
            new_value = cls.enter_period()
        elif choice == "target": 
            print (f"The new target must be greater than the current streak of {habit_to_adjust.streak}.")
            while True: 
                new_value = cls.enter_valid_target() 
                if new_value > habit_to_adjust.streak: 
                    break 
                else: print(f"Invalid input. The new target must be greater than the current streak of {habit_to_adjust.streak}.")
    
        
        if habit_to_adjust:
            setattr(habit_to_adjust, choice, new_value)
            print(f"Habit No. {habit_id} has been adjusted. {choice} is now {new_value}.")

# CHECK habit
    @classmethod
    def check(cls, habits):
        if cls.check_habits_exist(habits):
            return
        
        habit_id = cls.check_id_exists(habits, occasion_name="check")
        if habit_id is None:
            return
        
        confirmation = questionary.confirm(f"Do you really want to check habit no. {habit_id}?").ask()
        if confirmation:
            habit_to_check = next((habit for habit in habits if habit.id_h == habit_id), None)

            if habit_to_check.status == "Established":
                print("This habit is already established. If you want to re-establish this habit, you can use the “Duplicate” function.")
                return
            else:
                habit_to_check.streak += 1
                habit_to_check.streak_max = max(habit_to_check.streak_max, habit_to_check.streak)
                habit_to_check.date_check.append(datetime.now().strftime("%Y-%m-%d"))  # Date check = current date
                habit_to_check.deadline = (datetime.now() + timedelta(days=habit_to_check.period)).strftime("%Y-%m-%d")
                
                if habit_to_check.streak == habit_to_check.target:
                    habit_to_check.status = "Established"  # Established. Broken and Active are handled in UPDATE
                    print("You have established this habit. Congratulations!")

                else:
                    print(f"{habit_to_check.name} has been checked. Next due date is {habit_to_check.deadline}.")

# DELETE habit
    @classmethod
    def delete(cls, habits):
        if cls.check_habits_exist(habits):
            return
        
        habit_id = cls.check_id_exists(habits, occasion_name="delete")
        if habit_id is None:
            return
        
        confirmation = questionary.confirm(f"Do you really want to delete habit no. {habit_id}?").ask()
        if confirmation:
            habit_to_delete = next((habit for habit in habits if habit.id_h == habit_id), None)
            habits.remove(habit_to_delete)
            print(f"Habit no. {habit_id} has been deleted.")

# DUPLICATE habit 
    @classmethod 
    def duplicate(cls, habits):
        print("Dublicate") 
        if cls.check_habits_exist(habits): 
            return
         
        habit_id = cls.check_id_exists(habits, occasion_name="duplicate") 
        if habit_id is None: 
            return 
        
        habit_to_duplicate = next((habit for habit in habits if habit.id_h == habit_id), None) 
        if habit_to_duplicate: 
            id_h = cls.get_id(habits) 
            name = questionary.text("Please enter the name of your new habit:").ask() 
            category = habit_to_duplicate.category 
            period = habit_to_duplicate.period 
            target = habit_to_duplicate.target

            new_habit = cls(id_h, name, category, period, target)

            habits.append(new_habit) 
            print(f"Habit no. {habit_id} has been duplicated.")

# UPDATE habits
    @classmethod
    def update(cls, habits):
        for habit in habits:
            if habit.status != "Established":  # Only habits which are not yet established. Establishment during CHECK.
                now = datetime.now().strftime("%Y-%m-%d")

                if habit.deadline < now:
                    habit.status = "Broken"  # habit is now broken
                    habit.streak = 0  # streak is reset
                    if len(habit.interruptions) == 0 or max(habit.interruptions) != now:
                        habit.interruptions.append(datetime.now().strftime("%Y-%m-%d"))
                else:
                    habit.status = "Active"  # habit is now active

    @staticmethod
    def get_id(habits):
        id_h = 1
        if habits:
            id_h = max(habit.id_h for habit in habits) + 1
        return id_h

    @staticmethod
    def enter_category():
        category = questionary.select(
            "Which of these categories does your new habit belong to?",
            choices=categories
        ).ask()
        return category

    @staticmethod
    def enter_period():
        period_word = questionary.select(
            "In which period you want to repeat your new habit?",
            choices=periods
        ).ask()
        period = {"Daily": 1, "Every two days": 2, "Weekly": 7}[period_word]
        return period

    @staticmethod
    def enter_valid_target():
        while True:
            try:
                target = int(questionary.text("How many times do you want to repeat that habit?").ask())
                if target > 0:
                    return target
                else:
                    print("Invalid input. Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    @staticmethod
    def check_habits_exist(habits):
        if not habits:
            print("No habits found. You can add new habits by using the “ADD“ function.")
            return True
        return False

    @staticmethod
    def check_id_exists(habits, occasion_name):
        try:
            habit_id = int(questionary.text(f"Please enter the ID of the habit you want to {occasion_name}:").ask())
        except ValueError:
            print("Invalid input. Please enter one of the numeric IDs you can see in the list above.")
            return None
        
        if not any(habit.id_h == habit_id for habit in habits):
            print(f"No habit found with ID {habit_id}. Please enter a numeric ID you can see in the list above.")
            return None
        
        return habit_id