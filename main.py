import questionary

from manage import Habit

from analyse import Analyse
import display
from store import HabitsStore

habits_store = HabitsStore()
habits = habits_store.load()
Habit.update(habits)

print ("Welcome to Habit Tracker 2024.\n")
if not Habit.check_habits_exist(habits):
    print ("Here are your current habits:")
    display.display_habits(habits, status_request = "Established", length = "short")
  
# Main Menu
def cli_main(): 
    while True:
        print(f"\n \\\ MAIN MENU // ")
        choice = questionary.select(
            "\n What do you want to do?",
            choices=["Quick Check", "Add", "Manage", "Analyse", "Exit"]
        ).ask()

        if choice == "Quick Check":
            check()
                    
        elif choice == "Add":
            Habit.add(habits)

        elif choice == "Manage":
            cli_sub1()        

        elif choice == "Analyse":
            cli_sub2()

        elif choice == "Exit":
            habits_store.save(habits, filename="habits.json")
            print("Thanks for using Habit Tracker. Keep on tracking and see you soon!")
            break

## Submenu for choice MANAGE
def cli_sub1(): 
    while True:
        print(f"\n \\\ SUB MENU - MANAGE // ")
        choice = questionary.select(
            "What do you want to do?",
            choices=["Filter", "Check", "Delete", "Duplicate", "Adjust", "Back"]
        ).ask()
        
        if choice == "Filter":
            display.filter_indiv(habits)

        elif choice == "Check":
            check()

        elif choice == "Delete":
            display.display_habits(habits, status_request = None,  length = "full")
            Habit.delete(habits)

        elif choice == "Duplicate":
            display.display_habits(habits, status_request = None,  length = "full")
            Habit.duplicate(habits)
            
        elif choice == "Adjust":
            display.display_habits(habits, status_request = "Established",  length = "full")
            Habit.adjust(habits)

        else: # back was chosen
            print("Back to Main Menu")
            break

## Submenu for choice ANALYSE 
def cli_sub2(): 
    while True:
        print(f"\n \\\ SUB MENU - ANALYSE //")
        choice = questionary.select(
            "What do you want to do?",
            choices=["Longest active streaks", "Longest maximum streak", "Most interruptions", "Longest expired", "Group by category", "Established", "Broken", "Back"]
        ).ask()
        
        if choice == "Longest active streaks":
            Analyse.get_top_main(habits, attribute = "streak", attribute_name = "Streak", attribute_descriptions = "longest streak")
        elif choice == "Longest maximum streak":
            Analyse.get_top_main(habits, attribute = "streak_max", attribute_name = "Max streak", attribute_descriptions = "longest max streak")
        elif choice == "Most interruptions":
            Analyse.get_top_most_interruptions(habits)
        elif choice == "Longest expired":
            Analyse.get_top_longestExpired(habits)

        elif choice == "Group by category":
            Analyse.get_group_habitsByCategory(habits)

        elif choice == "Established":
            Analyse.get_all_main(habits, status = 2 , status_name = "Established")
        elif choice == "Broken":
            Analyse.get_all_main(habits, status = -1 , status_name = "Broken")

        else: # back was chosen
            print("Back to Main Menu")
            break

def check():
    print("Here are all active and broken habits:")
    display.display_habits(habits, status_request = "Established", length = "short")
    Habit.check(habits)

if __name__ == "__main__":
    cli_main()
