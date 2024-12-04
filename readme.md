# Habit Tracker 2024

With this application, you will never fail to track your habits anymore.

## What is it?

Habit Tracker is a simple and effective application designed to help you track and maintain your habits effortlessly. Whether you want to build new habits or break old ones, this tool is here to support you.

## Features

- **Track multiple habits:** Monitor and track the progress of various habits simultaneously.
- **Reminders:** Set reminders to ensure you never forget a habit.
- **Detailed statistics:** Visualize your progress with charts and graphs.
- **Customization:** Customize habit categories, frequencies, and reminders to suit your needs.

## Installation

To install the necessary dependencies, use the following command:

```shell
pip install -r requirements.txt
```

## Usage

Start the application by running the main script and follow the instructions provided:
```shell
python main.py
```
**Main Menu Options**
- **Quick Check:** Check the status of your habits.
- **Add:** Add a new habit to track.
- **Manage:** Manage your existing habits with options to filter, check, delete, duplicate, or adjust them.
- **Analyse:** Analyse your habits with various metrics such as longest active streaks, most interruptions, etc.
- **Exit:** Save your progress and exit the application.

**Code Structure**
- **main.py:** Contains the main logic of the application including the command-line interface.
- **manage.py:** Contains the Habit class and associated methods for habit management.
- **display.py:** Functions to display and filter habits using tabulate.
- **analyse.py:** Functions to analyze habits and provide detailed statistics.
- **store.py:** Functions to load and save habits data.

## Tests

```shell
pytest .
```

## Current Version
04/12/2024