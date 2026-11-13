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
- Keyboard support: **A–D** (or **1–4**) to choose an option, **Enter** for Next
- Input checks: the player name is required and limited to 20 characters
- Confirmation pop-ups before leaving or quitting a quiz in progress

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
| Menu | File and Help menus |
| messagebox | Errors, warnings and confirmations |
| Events (`bind`, `after`, `command`, `protocol`) | Keyboard keys, hover effect, timer, button clicks, window close |

## How to run

Requires **Python 3.8 or newer**. Tkinter comes with Python on Windows and macOS, so nothing extra needs installing.

```
python quiz_app.py
```

On Linux, install Tkinter first: `sudo apt install python3-tk`

## Project structure

```
quiz_app.py       the application (question bank included)
README.md
```

## Editing the questions

The questions are stored in the `QUESTIONS` dictionary at the top of `quiz_app.py`.
Each category maps to a list of tuples in this format:

```python
(question text, [option 1, option 2, option 3, option 4], index of the correct option)
```

Example:

```python
"Python": [
    ("Which keyword is used to define a function in Python?", ["function", "def", "fun", "define"], 1),
]
```

The index starts from 0, so `1` means the second option (`"def"`).
Save the file and run the app again. A new top-level key in `QUESTIONS` creates a new category.

## Author

Shaurya Singh – B.Tech CSE (AI/ML), SRMIST Kattankulathur
