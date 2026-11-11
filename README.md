# Smart Quiz App

A desktop quiz application built with **Python and Tkinter**.
Course project for **21CSC203P – Advanced Programming Practice** (Unit 5: Event Programming Paradigm),
SRM Institute of Science and Technology, Kattankulathur.

## Features

- Three categories: **Python**, **Java Basics** and **Unit 5 Concepts** (15 questions each)
- Choose the number of questions, the time per question, and whether to shuffle questions and options
- Countdown timer bar that turns red when time is almost over
- Instant feedback: the correct option turns green, a wrong pick turns red
- Result screen with a pie chart, and an **answer review** screen showing every question
- Light and dark theme (View → Dark mode)
- Keyboard support: **A–D** to choose an option, **Enter** for Next
- Questions are loaded from `questions.json`; built-in questions are used if the file is missing or broken
- Safe error handling: invalid questions are skipped and reported instead of crashing the app

## Tkinter concepts used

| Concept | Where it is used |
|---|---|
| `Tk()`, `mainloop()` | Main window and event loop |
| `pack()`, `grid()`, `place()` | All three geometry managers |
| Label, Button, Entry | Name field, buttons, text |
| Radiobutton, Checkbutton | Answer options, settings |
| Scale, Spinbox, Combobox | Seconds per question, number of questions, category |
| Canvas | Timer bar and result pie chart |
| Text + Scrollbar | Answer review |
| Menu | File, View and Help menus |
| messagebox | Errors, warnings and confirmations |
| Events (`bind`, `after`, `command`) | Keyboard keys, hover effect, timer, button clicks |

## How to run

Requires **Python 3.8 or newer**. Tkinter comes with Python on Windows and macOS, so nothing extra needs installing.

```
python quiz_app.py
```

On Linux, install Tkinter first: `sudo apt install python3-tk`

## Project structure

```
quiz_app.py       the application
questions.json    the question bank
README.md
```

## Editing the questions

Open `questions.json` and add or change questions. Each question needs a text, exactly 4 different options,
and an `answer` that matches one of the options exactly:

```json
{
  "Python": [
    {
      "question": "Which keyword is used to define a function in Python?",
      "options": ["function", "def", "fun", "define"],
      "answer": "def"
    }
  ]
}
```

Save the file and use **File → Reload Questions** in the app (no restart needed).
A new top-level name creates a new category.

## Author

Shaurya Singh – B.Tech CSE (AI/ML), SRMIST Kattankulathur
