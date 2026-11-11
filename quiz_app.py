"""
SMART QUIZ APP - Tkinter
Course : 21CSC203P Advanced Programming Practice (Unit 5 - Event Programming Paradigm)

Flow   : Home -> Quiz (timer, instant feedback) -> Result (pie chart) -> Answer Review
Data   : questions are read from questions.json (built-in questions are used if the file is unusable)
"""
import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# ======================================================================
# 1. QUESTION DATA  (kept separate from the GUI code)
# ======================================================================
QUESTION_FILE = Path(__file__).with_name("questions.json")   # same folder as this script

# Built-in fallback -> category : [(question, [4 options], index of correct option)]
DEFAULT_QUESTIONS = {
    "Python": [
        ("Which keyword is used to define a function in Python?", ["function", "def", "fun", "define"], 1),
        ("What is the output of type([])?", ["<class 'tuple'>", "<class 'dict'>", "<class 'list'>", "<class 'set'>"], 2),
        ("Which of these data types is immutable?", ["list", "dict", "set", "tuple"], 3),
        ("What does len('SRM') return?", ["2", "3", "4", "SRM"], 1),
        ("Which symbol starts a single-line comment in Python?", ["//", "/*", "#", "--"], 2),
        ("What does range(3) generate?", ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"], 1),
        ("Which block is used for exception handling?", ["try-except", "if-else", "for-while", "def-return"], 0),
        ("What is the value of 2 ** 3?", ["6", "5", "8", "9"], 2),
        ("Which list method adds an item at the end?", ["add()", "insert()", "append()", "push()"], 2),
        ("Which library is widely used for DataFrames?", ["pandas", "tkinter", "random", "sympy"], 0),
        ("Which function is used to take input from the user?", ["scan()", "input()", "read()", "get()"], 1),
        ("Which brackets are used to create a dictionary?", ["[ ]", "( )", "{ }", "< >"], 2),
        ("What does the 'break' statement do inside a loop?", ["Skips one round", "Stops the loop", "Restarts the loop", "Ends the program"], 1),
        ("Which keyword is used to bring in a module?", ["include", "import", "using", "load"], 1),
        ("What is the output of 7 % 3?", ["2", "1", "3", "0"], 1),
    ],
    "Java Basics": [
        ("Which keyword is used to create an object in Java?", ["make", "new", "create", "object"], 1),
        ("From which method does a Java program start running?", ["start()", "run()", "main()", "init()"], 2),
        ("Which of these is NOT a primitive data type?", ["int", "char", "boolean", "String"], 3),
        ("Which keyword is used to inherit a class?", ["extends", "inherits", "implements", "super"], 0),
        ("How many bytes does an int take in Java?", ["2", "4", "8", "1"], 1),
        ("Which keyword makes a variable a constant?", ["static", "const", "final", "fixed"], 2),
        ("What is the output of 10 / 3 for two int values?", ["3.33", "3", "4", "1"], 1),
        ("Which loop always runs at least once?", ["for", "while", "do-while", "foreach"], 2),
        ("Java source code is first compiled into...", ["machine code", "bytecode", "assembly", "HTML"], 1),
        ("Which statement prints a line in Java?", ["print()", "echo()", "System.out.println()", "console.log()"], 2),
        ("Which keyword is used to create a class in Java?", ["class", "new", "struct", "define"], 0),
        ("Array indexing in Java starts from...", ["0", "1", "-1", "2"], 0),
        ("Which block is used to handle exceptions in Java?", ["try-catch", "if-else", "switch", "for"], 0),
        ("Which method gives the length of a String?", ["size()", "length()", "len()", "count()"], 1),
        ("Which keyword is used to implement an interface?", ["extends", "implements", "inherits", "uses"], 1),
    ],
    "Unit 5 Concepts": [
        ("Which method starts the Tkinter event loop?", ["start()", "run()", "mainloop()", "loop()"], 2),
        ("Which widget is used to show text on the window?", ["Label", "Canvas", "Scale", "Spinbox"], 0),
        ("Which widget allows only ONE choice from many?", ["Checkbutton", "Entry", "Radiobutton", "Label"], 2),
        ("Which widget is used to draw shapes and lines?", ["Label", "Canvas", "Spinbox", "Button"], 1),
        ("Which geometry manager uses rows and columns?", ["pack()", "grid()", "place()", "align()"], 1),
        ("A function that runs when a button is clicked is called...", ["Event handler", "Constructor", "Loop", "Module"], 0),
        ("DFA stands for...", ["Dynamic Final Array", "Deterministic Finite Automaton", "Direct File Access", "Digital Flow Analysis"], 1),
        ("Which Python library is used for symbolic maths?", ["SymPy", "Tkinter", "Random", "Turtle"], 0),
        ("Which SymPy function finds the derivative?", ["integrate()", "diff()", "solve()", "expand()"], 1),
        ("In event-driven programming, the program flow is decided by...", ["Events like clicks and key presses", "Only loops", "Only functions", "Only classes"], 0),
        ("Which widget gives a single-line text box?", ["Entry", "Label", "Canvas", "Scale"], 0),
        ("Which widget is a slider used to pick a number?", ["Entry", "Scale", "Menu", "Label"], 1),
        ("Which call shows a pop-up message in Tkinter?", ["messagebox.showinfo()", "print()", "mainloop()", "pack()"], 0),
        ("Which SymPy function expands (x + y)**2?", ["simplify()", "expand()", "solve()", "limit()"], 1),
        ("Compared to a DFA, an NFA can have...", ["Many transitions for the same symbol", "Only one transition", "No states", "No input symbols"], 0),
    ],
}


def parse_question(item):
    """Check ONE question taken from the JSON file and convert it to (text, options, answer_index).
    Raises ValueError with a short reason when the question is not valid."""
    if not isinstance(item, dict):
        raise ValueError("must be an object with question / options / answer")
    text = str(item.get("question", "")).strip()
    options = item.get("options")
    answer = str(item.get("answer", "")).strip()
    if not text:
        raise ValueError("'question' is missing")
    if not isinstance(options, list) or len(options) != 4:
        raise ValueError("'options' must be a list of exactly 4 items")
    options = [str(o).strip() for o in options]
    if "" in options or len(set(options)) != 4:
        raise ValueError("options must be 4 different, non-empty texts")
    if answer not in options:
        raise ValueError("'answer' must be exactly one of the options")
    return text, options, options.index(answer)


def load_questions(path=QUESTION_FILE):
    """Read the question file. Returns (bank, notes).
    bank  = {category: [(text, options, answer_index), ...]}
    notes = list of problems found (shown to the user). Falls back to DEFAULT_QUESTIONS if needed."""
    try:
        with open(path, encoding="utf-8") as file:           # 'with' closes the file automatically
            raw = json.load(file)                            # JSON text -> Python dict/list
    except FileNotFoundError:
        return DEFAULT_QUESTIONS, []                         # no file: quietly use built-in questions
    except json.JSONDecodeError as err:
        return DEFAULT_QUESTIONS, [f"{Path(path).name} has a syntax error (line {err.lineno}).",
                                   "Built-in questions are being used."]
    except (OSError, UnicodeDecodeError) as err:
        return DEFAULT_QUESTIONS, [f"{Path(path).name} could not be read ({type(err).__name__}).",
                                   "Built-in questions are being used."]

    if not isinstance(raw, dict):
        return DEFAULT_QUESTIONS, [f"{Path(path).name} must contain categories at the top level.",
                                   "Built-in questions are being used."]
    bank, notes = {}, []
    for category, items in raw.items():
        if not isinstance(items, list):
            notes.append(f"Category '{category}' skipped: it must be a list of questions.")
            continue
        valid = []
        for number, item in enumerate(items, start=1):
            try:
                valid.append(parse_question(item))
            except ValueError as err:                        # skip the bad question, keep the rest
                notes.append(f"{category} #{number} skipped: {err}.")
        if valid:
            bank[category] = valid
    if not bank:
        return DEFAULT_QUESTIONS, notes + ["No valid questions found. Built-in questions are being used."]
    return bank, notes


def shuffle_options(question):
    """Return a copy of the question with its options in random order (answer index updated)."""
    text, options, answer = question
    correct_text = options[answer]
    options = options[:]
    random.shuffle(options)
    return text, options, options.index(correct_text)


def format_notes(notes, limit=6):
    """Join problem messages for a message box (long lists are shortened)."""
    shown = notes[:limit]
    if len(notes) > limit:
        shown.append(f"...and {len(notes) - limit} more.")
    return "\n".join(shown)


# ======================================================================
# 2. LOOK AND FEEL
# ======================================================================
THEMES = {
    "light": dict(bg="#f4f1fb", fg="#222222", accent="#4B0082", card="#ffffff",
                  track="#dddddd", muted="#888888", good="#2e7d32", bad="#c62828",
                  sel="#d9c8f5", hover="#efe9fb", border="#d0c8e6"),
    "dark":  dict(bg="#1e1e2e", fg="#eeeeee", accent="#b39ddb", card="#2b2b3c",
                  track="#3a3a4e", muted="#777777", good="#81c784", bad="#ef9a9a",
                  sel="#5b4b9a", hover="#363650", border="#44445c"),
}
GREEN, RED, BLUE, PURPLE = "#4CAF50", "#f44336", "#2196F3", "#6A1B9A"
FONT = ("Arial", 12)
LETTERS = "ABCD"          # labels for the 4 options
BAR_WIDTH = 440           # width of the timer bar (pixels)
FEEDBACK_MS = 1000        # how long green/red feedback is shown (milliseconds)
MAX_NAME = 20             # longest allowed player name
WIN_W, WIN_H = 620, 560   # window size (pixels)


# ======================================================================
# 3. APPLICATION
# ======================================================================
class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Quiz App")
        self.center_window()
        root.resizable(False, False)

        self.bank, notes = load_questions()

        # Tkinter variables: automatically linked to widgets (Entry, Combobox, Scale, ...)
        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar(value=next(iter(self.bank)))
        self.count_var = tk.StringVar(value="5")
        self.sec_var = tk.IntVar(value=20)
        self.shuffle_var = tk.IntVar(value=1)
        self.timer_var = tk.IntVar(value=1)
        self.dark_var = tk.IntVar(value=0)       # 0 = light, 1 = dark
        self.choice = tk.IntVar(value=-1)        # selected option (-1 = nothing)

        self.frame = None          # the screen currently shown
        self.screen = "home"       # "home" / "quiz" / "result" / "review"
        self.timer_job = None      # id returned by after(), needed to cancel it
        self.locked = False        # True while green/red feedback is being shown
        self.use_timer = True      # settings fixed when a quiz starts
        self.time_total = self.time_left = 0
        self.questions, self.answers = [], []
        self.index = self.score = 0

        self.apply_theme()
        self.build_menu()
        self.show_home()

        # EVENT BINDING: keyboard events handled by our own functions
        root.bind("<Return>", self.on_enter)                 # Enter -> Next / Start
        root.bind("<Key>", self.on_key)                      # A-D   -> choose option
        root.protocol("WM_DELETE_WINDOW", self.quit_app)     # window close button (X)

        if notes:                                            # problems found in questions.json
            root.after(300, lambda: messagebox.showwarning("Question file", format_notes(notes)))

    def center_window(self):
        """Open the window in the middle of the screen instead of the top-left corner."""
        self.root.update_idletasks()
        x = max(0, (self.root.winfo_screenwidth() - WIN_W) // 2)
        y = max(0, (self.root.winfo_screenheight() - WIN_H) // 2 - 30)    # -30 leaves room for the taskbar
        self.root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    # ---------------------------------------------------------- THEME
    def apply_theme(self):
        self.t = THEMES["dark" if self.dark_var.get() else "light"]
        t = self.t
        self.root.configure(bg=t["bg"])
        style = ttk.Style()
        style.theme_use("clam")                  # 'clam' lets us colour the Combobox
        style.configure("TCombobox", fieldbackground=t["card"], background=t["card"],
                        foreground=t["fg"], arrowcolor=t["fg"])
        style.map("TCombobox", fieldbackground=[("readonly", t["card"])],
                  foreground=[("readonly", t["fg"])],
                  selectbackground=[("readonly", t["card"])],
                  selectforeground=[("readonly", t["fg"])])
        self.root.option_add("*TCombobox*Listbox.background", t["card"])
        self.root.option_add("*TCombobox*Listbox.foreground", t["fg"])

    def toggle_theme(self):
        """Menu -> View -> Dark mode : apply colours and redraw the current screen."""
        self.apply_theme()
        if self.screen == "quiz":
            if self.locked:                      # feedback showing; new colours appear on next question
                return
            left = self.time_left if self.use_timer else None
            self.show_question(resume=(self.choice.get(), left))
        else:
            {"home": self.show_home, "result": self.show_result, "review": self.show_review}[self.screen]()

    # ---------------------------------------------------------- MENU
    def build_menu(self):
        bar = tk.Menu(self.root)
        file_menu = tk.Menu(bar, tearoff=0)
        file_menu.add_command(label="New Quiz", command=self.new_quiz)
        file_menu.add_command(label="Reload Questions", command=self.reload_questions)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)
        bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(bar, tearoff=0)
        view_menu.add_checkbutton(label="Dark mode", variable=self.dark_var, command=self.toggle_theme)
        bar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(bar, tearoff=0)
        help_menu.add_command(label="How to play", command=lambda: messagebox.showinfo(
            "How to play",
            "1. Enter your name and choose a category.\n"
            "2. Click an option card (or press A-D).\n"
            "3. Press Enter / Next before the timer bar runs out.\n"
            "4. Green = correct answer, red = your wrong answer.\n"
            "5. At the end, see the pie chart and review all answers.\n\n"
            "Questions live in questions.json - edit it, then use File > Reload Questions."))
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
            "About", "Smart Quiz App\nPython + Tkinter\n21CSC203P - Unit 5"))
        bar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=bar)

    def new_quiz(self):
        if self.screen != "quiz" or messagebox.askyesno("New Quiz", "Leave this quiz and go to Home?"):
            self.show_home()

    def reload_questions(self):
        """Read questions.json again without restarting the app."""
        if self.screen != "home":
            messagebox.showinfo("Reload Questions", "Please go to the Home screen first (File > New Quiz).")
            return
        self.bank, notes = load_questions()
        if self.category_var.get() not in self.bank:
            self.category_var.set(next(iter(self.bank)))
        self.show_home()                                     # redraw so the category list is updated
        total = sum(len(items) for items in self.bank.values())
        message = f"Loaded {total} questions in {len(self.bank)} categories."
        messagebox.showinfo("Reload Questions", message + ("\n\n" + format_notes(notes) if notes else ""))

    def quit_app(self):
        """Used by the X button, File > Exit and the Exit button."""
        if self.screen == "quiz" and not messagebox.askyesno("Quit", "A quiz is in progress. Do you really want to quit?"):
            return
        self.cancel_timer()
        self.root.destroy()

    # ---------------------------------------------------------- HELPERS (avoid repeating code)
    def new_screen(self):
        """Destroy the old screen and return a fresh Frame (pack with fill/expand)."""
        self.cancel_timer()
        self.locked = False
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, bg=self.t["bg"])
        self.frame.pack(fill="both", expand=True)
        return self.frame

    def cancel_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def lbl(self, parent, text, size=12, bold=False, color=None, **kw):
        return tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                        fg=color or self.t["fg"], bg=self.t["bg"], **kw)

    def btn(self, parent, text, command, color=GREEN, width=12, size=12):
        return tk.Button(parent, text=text, command=command, bg=color, fg="white",
                         activebackground=color, activeforeground="white", relief="flat",
                         font=("Arial", size, "bold"), width=width, cursor="hand2")

    def check(self, parent, text, var):
        t = self.t
        return tk.Checkbutton(parent, text=text, variable=var, font=FONT, bg=t["bg"], fg=t["fg"],
                              selectcolor=t["card"], activebackground=t["bg"], activeforeground=t["fg"])

    # ---------------------------------------------------------- HOME SCREEN
    def show_home(self):
        self.screen = "home"
        t = self.t
        f = self.new_screen()
        self.lbl(f, "SMART QUIZ APP", 24, True, t["accent"]).pack(pady=(30, 2))
        self.lbl(f, "Test yourself and see how much you know").pack(pady=(0, 15))

        form = tk.Frame(f, bg=t["bg"])
        form.pack(pady=5)                       # widgets inside 'form' use grid()

        def label(text, row):
            self.lbl(form, text).grid(row=row, column=0, sticky="e", padx=10, pady=8)

        label("Your Name:", 0)                  # Entry
        tk.Entry(form, textvariable=self.name_var, font=FONT, width=24, bg=t["card"], fg=t["fg"],
                 insertbackground=t["fg"], relief="solid", bd=1).grid(row=0, column=1, sticky="w")

        label("Category:", 1)                   # Combobox (dropdown)
        ttk.Combobox(form, textvariable=self.category_var, values=list(self.bank),
                     state="readonly", font=FONT, width=22).grid(row=1, column=1, sticky="w")

        label("No. of Questions:", 2)           # Spinbox
        tk.Spinbox(form, from_=3, to=15, textvariable=self.count_var, width=6, font=FONT,
                   state="readonly", readonlybackground=t["card"], fg=t["fg"],
                   buttonbackground=t["card"]).grid(row=2, column=1, sticky="w")

        label("Seconds / Question:", 3)         # Scale (slider)
        tk.Scale(form, from_=10, to=60, resolution=5, orient="horizontal", length=190,
                 variable=self.sec_var, bg=t["bg"], fg=t["fg"], troughcolor=t["track"],
                 highlightthickness=0).grid(row=3, column=1, sticky="w")

        label("Options:", 4)                    # Checkbuttons (ON/OFF)
        self.check(form, "Shuffle questions and options", self.shuffle_var).grid(row=4, column=1, sticky="w")
        self.check(form, "Enable timer", self.timer_var).grid(row=5, column=1, sticky="w")

        self.btn(f, "START QUIZ", self.start_quiz, GREEN, 16, 13).pack(pady=20)

    def start_quiz(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return
        if len(name) > MAX_NAME:
            messagebox.showerror("Error", f"Name must be at most {MAX_NAME} characters.")
            return
        pool = list(self.bank.get(self.category_var.get(), []))
        if not pool:
            messagebox.showerror("Error", "No questions found in this category.")
            return
        try:
            count = int(self.count_var.get())
        except ValueError:
            count = 5
        if self.shuffle_var.get():
            random.shuffle(pool)                              # shuffle question order
            pool = [shuffle_options(q) for q in pool]         # shuffle option order
        self.questions = pool[:max(1, min(count, len(pool)))]    # never more than the category has
        self.use_timer = bool(self.timer_var.get())
        self.time_total = self.sec_var.get()
        self.index, self.score, self.answers = 0, 0, []
        self.show_question()

    # ---------------------------------------------------------- QUIZ SCREEN
    def show_question(self, resume=None):
        """resume = (selected option, time left) -> used only when the theme is switched mid-question."""
        self.screen = "quiz"
        t = self.t
        f = self.new_screen()
        question, options, _ = self.questions[self.index]
        self.choice.set(resume[0] if resume else -1)

        self.lbl(f, f"Question {self.index + 1} of {len(self.questions)}", 11, True, t["accent"]).pack(pady=(15, 5))
        # place(): exact position -> score fixed at top-right corner
        self.score_lbl = self.lbl(f, f"Score: {self.score}", 11, True)
        self.score_lbl.place(relx=1.0, x=-15, y=12, anchor="ne")

        if self.use_timer:                      # CANVAS: timer bar that shrinks every second
            row = tk.Frame(f, bg=t["bg"])
            row.pack(pady=5)
            self.bar = tk.Canvas(row, width=BAR_WIDTH, height=14, bg=t["track"], highlightthickness=0)
            self.bar.pack(side="left")
            self.bar_rect = self.bar.create_rectangle(0, 0, BAR_WIDTH, 14, fill=GREEN, width=0)
            self.time_lbl = self.lbl(row, "", 11, True, width=5)
            self.time_lbl.pack(side="left", padx=(8, 0))
            self.time_left = resume[1] if resume and resume[1] is not None else self.time_total

        # question inside its own "card"
        card = tk.Frame(f, bg=t["card"], highlightthickness=1, highlightbackground=t["border"])
        card.pack(fill="x", padx=40, pady=(12, 14))
        tk.Label(card, text=question, font=("Arial", 14, "bold"), wraplength=500, justify="left",
                 bg=t["card"], fg=t["fg"], padx=16, pady=16).pack(anchor="w")

        self.opts = []
        for i, text in enumerate(options):      # RADIOBUTTONS drawn as clickable cards (indicatoron=0)
            rb = tk.Radiobutton(f, text=f"   {LETTERS[i]}.    {text}", variable=self.choice, value=i,
                                indicatoron=0, font=FONT, bg=t["card"], fg=t["fg"],
                                selectcolor=t["sel"], activebackground=t["hover"], activeforeground=t["fg"],
                                anchor="w", justify="left", wraplength=470, width=46, padx=10, pady=8,
                                relief="flat", offrelief="flat", bd=0, highlightthickness=1,
                                highlightbackground=t["border"], highlightcolor=t["accent"], cursor="hand2")
            rb.pack(pady=4)
            # EVENTS: highlight the card when the mouse enters / leaves it
            rb.bind("<Enter>", lambda e, w=rb: None if self.locked else w.config(bg=t["hover"]))
            rb.bind("<Leave>", lambda e, w=rb: None if self.locked else w.config(bg=t["card"]))
            self.opts.append(rb)

        self.fb = self.lbl(f, " ", 12, True)    # feedback message (Correct / Wrong)
        self.fb.pack(pady=(10, 0))
        last = self.index == len(self.questions) - 1
        self.next_btn = self.btn(f, "Finish" if last else "Next", self.next_question)
        self.next_btn.pack(pady=10)
        self.lbl(f, "Tip: press A-D to choose an option and Enter for Next", 10,
                 color=t["muted"]).pack(side="bottom", pady=8)

        if self.use_timer:                      # start the timer LAST, when every widget exists
            self.tick()

    def tick(self):
        """Called every 1 second using after() - runs without freezing the window."""
        low = self.time_left <= self.time_total * 0.25
        self.bar.coords(self.bar_rect, 0, 0, BAR_WIDTH * self.time_left / self.time_total, 14)
        self.bar.itemconfig(self.bar_rect, fill=RED if low else GREEN)
        self.time_lbl.config(text=f"{self.time_left}s", fg=self.t["bad"] if low else self.t["fg"])
        if self.time_left <= 0:
            self.next_question(timed_out=True)  # time over -> check automatically
        else:
            self.time_left -= 1
            self.timer_job = self.root.after(1000, self.tick)

    def next_question(self, timed_out=False):
        if self.screen != "quiz" or self.locked:    # ignore clicks while feedback is showing
            return
        picked = self.choice.get()
        if picked == -1 and not timed_out:
            messagebox.showwarning("Select an option", "Please choose an answer first.")
            return
        correct = self.questions[self.index][2]
        self.answers.append(picked)             # saved for the review screen
        self.locked = True
        self.cancel_timer()
        if picked == correct:
            self.score += 1
        self.score_lbl.config(text=f"Score: {self.score}")
        self.show_feedback(picked, correct)
        self.timer_job = self.root.after(FEEDBACK_MS, self.advance)   # show colours, then move on

    def show_feedback(self, picked, correct):
        """Correct option turns green, a wrong pick turns red, all options get disabled."""
        t = self.t
        for i, rb in enumerate(self.opts):
            rb.config(state="disabled", disabledforeground=t["muted"], bg=t["card"])
            if i == correct:
                rb.config(bg=GREEN, selectcolor=GREEN, disabledforeground="white")
            elif i == picked:
                rb.config(bg=RED, selectcolor=RED, disabledforeground="white")
        self.next_btn.config(state="disabled")
        if picked == correct:
            self.fb.config(text="Correct!", fg=t["good"])
        elif picked == -1:
            self.fb.config(text="Time's up!", fg=t["bad"])
        else:
            self.fb.config(text="Wrong!", fg=t["bad"])

    def advance(self):
        self.timer_job = None
        self.index += 1
        if self.index < len(self.questions):
            self.show_question()
        else:
            self.show_result()

    # ---------------------------------------------------------- RESULT SCREEN
    def show_result(self):
        self.screen = "result"
        t = self.t
        f = self.new_screen()
        total = len(self.questions)
        percent = self.score / total * 100

        self.lbl(f, "Quiz Completed!", 22, True, t["accent"]).pack(pady=(25, 5))
        self.lbl(f, f"{self.name_var.get().strip()}, you scored {self.score} / {total}  ({percent:.0f}%)", 13).pack()
        remark = "Excellent!" if percent >= 80 else "Good job, keep practising!" if percent >= 50 else "Keep learning, try again!"
        self.lbl(f, remark, 13, True, t["good"] if percent >= 50 else t["bad"]).pack(pady=5)

        # CANVAS: pie chart drawn with create_arc()
        c = tk.Canvas(f, width=220, height=200, bg=t["bg"], highlightthickness=0)
        c.pack(pady=10)
        box = (30, 10, 190, 170)
        if self.score == total:                 # a 360-degree arc cannot be drawn, so use a circle
            c.create_oval(*box, fill=GREEN, outline="")
        elif self.score == 0:
            c.create_oval(*box, fill=RED, outline="")
        else:
            right = 360 * self.score / total
            c.create_arc(*box, start=90, extent=right, fill=GREEN, outline="")
            c.create_arc(*box, start=90 + right, extent=360 - right, fill=RED, outline="")
        c.create_rectangle(35, 181, 47, 193, fill=GREEN, outline="")
        c.create_text(52, 187, text="Correct", anchor="w", font=("Arial", 10), fill=t["fg"])
        c.create_rectangle(120, 181, 132, 193, fill=RED, outline="")
        c.create_text(137, 187, text="Wrong", anchor="w", font=("Arial", 10), fill=t["fg"])

        row = tk.Frame(f, bg=t["bg"])
        row.pack(pady=10)
        self.btn(row, "Review Answers", self.show_review, PURPLE, 14).pack(side="left", padx=6)
        self.btn(row, "Play Again", self.show_home, BLUE, 12).pack(side="left", padx=6)
        self.btn(row, "Exit", self.quit_app, RED, 10).pack(side="left", padx=6)

    # ---------------------------------------------------------- REVIEW SCREEN
    def show_review(self):
        """Text widget + Scrollbar showing every question, your answer and the correct answer."""
        self.screen = "review"
        t = self.t
        f = self.new_screen()
        self.lbl(f, "Answer Review", 20, True, t["accent"]).pack(pady=(15, 8))
        self.btn(f, "Back to Result", self.show_result, BLUE, 16).pack(side="bottom", pady=12)

        box = tk.Frame(f, bg=t["bg"])
        box.pack(fill="both", expand=True, padx=20)
        scroll = tk.Scrollbar(box)
        scroll.pack(side="right", fill="y")
        text = tk.Text(box, wrap="word", font=("Arial", 11), bg=t["card"], fg=t["fg"], relief="flat",
                       padx=10, pady=8, yscrollcommand=scroll.set)
        text.pack(side="left", fill="both", expand=True)
        scroll.config(command=text.yview)

        text.tag_config("q", font=("Arial", 11, "bold"))      # tags = coloured / bold text styles
        text.tag_config("good", foreground=t["good"])
        text.tag_config("bad", foreground=t["bad"])

        for i, (question, options, answer) in enumerate(self.questions):
            picked = self.answers[i]
            text.insert("end", f"Q{i + 1}. {question}\n", "q")
            if picked == answer:
                text.insert("end", f"Your answer: {options[picked]}  (Correct)\n\n", "good")
            else:
                mine = options[picked] if picked != -1 else "Not answered (time over)"
                text.insert("end", f"Your answer: {mine}  (Wrong)\n", "bad")
                text.insert("end", f"Correct answer: {options[answer]}\n\n", "good")
        text.config(state="disabled")                          # read-only

    # ---------------------------------------------------------- EVENT HANDLERS
    def on_enter(self, event):
        if self.screen == "quiz":
            self.next_question()
        elif self.screen == "home":
            self.start_quiz()

    def on_key(self, event):
        key = event.char.lower()
        if self.screen == "quiz" and not self.locked:
            if key in ("1", "2", "3", "4"):
                self.choice.set(int(key) - 1)
            elif key in ("a", "b", "c", "d"):
                self.choice.set("abcd".index(key))


if __name__ == "__main__":
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()