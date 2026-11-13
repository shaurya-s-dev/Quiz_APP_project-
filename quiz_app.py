import random
import tkinter as tk
from tkinter import messagebox, ttk

# category : [(question, [4 options], index of correct option)]
QUESTIONS = {
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

BG, ACCENT, GREEN, RED, BLUE, PURPLE = "#f4f1fb", "#4B0082", "#4CAF50", "#f44336", "#2196F3", "#6A1B9A"
HOVER, BORDER = "#efe9fb", "#d0c8e6"
FONT = ("Arial", 12)
CARD = dict(bg="white", highlightthickness=1, highlightbackground=BORDER)   # white box with a thin border
BAR = 440   # timer bar width in pixels


class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Quiz App")
        root.geometry("620x600")
        root.resizable(False, False)
        root.configure(bg=BG)

        # Tkinter variables linked to widgets
        self.name = tk.StringVar()
        self.category = tk.StringVar(value="Python")
        self.count = tk.StringVar(value="5")
        self.seconds = tk.IntVar(value=20)
        self.shuffle = tk.IntVar(value=1)
        self.timer_on = tk.IntVar(value=1)
        self.choice = tk.IntVar(value=-1)

        self.frame = self.job = None
        self.screen = "home"          # "home" / "quiz" / "result" / "review"
        self.locked = False           # True while green/red feedback is shown
        self.show_home()

        # Events
        root.bind("<Return>", self.on_enter)
        root.bind("<Key>", self.on_key)
        root.protocol("WM_DELETE_WINDOW", self.quit_app)

    # ---------------------------------------------------------- HELPERS
    def cancel(self):
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None

    def new_screen(self, name, title):
        """Fresh frame with a purple title banner on top."""
        self.screen, self.locked = name, False
        self.cancel()
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        tk.Label(self.frame, text=title, font=("Arial", 18, "bold"), bg=ACCENT, fg="white", pady=12).pack(fill="x")
        return self.frame

    def label(self, text, size=12, bold=False, color="black"):
        lbl = tk.Label(self.frame, text=text, font=("Arial", size, "bold" if bold else "normal"), bg=BG, fg=color)
        lbl.pack(pady=4)
        return lbl

    def button(self, parent, text, command, color=GREEN, side="top"):
        btn = tk.Button(parent, text=text, command=command, bg=color, fg="white", relief="flat",
                        font=("Arial", 12, "bold"), width=14, pady=4, cursor="hand2")
        btn.pack(side=side, padx=6, pady=8)
        return btn

    def quit_app(self):
        if self.screen == "quiz" and not messagebox.askyesno("Quit", "Quiz in progress. Quit anyway?"):
            return
        self.root.destroy()

    # ---------------------------------------------------------- HOME
    def show_home(self):
        f = self.new_screen("home", "SMART QUIZ APP")
        self.label("Test yourself and see how much you know").pack_configure(pady=(15, 0))

        card = tk.Frame(f, **CARD)
        card.pack(pady=20, ipadx=15, ipady=10)
        for row, text in enumerate(["Your Name:", "Category:", "No. of Questions:", "Seconds / Question:"]):
            tk.Label(card, text=text, font=FONT, bg="white").grid(row=row, column=0, sticky="e", padx=10, pady=8)

        tk.Entry(card, textvariable=self.name, font=FONT, width=24, relief="solid", bd=1).grid(row=0, column=1, sticky="w")
        ttk.Combobox(card, textvariable=self.category, values=list(QUESTIONS), state="readonly",
                     width=22).grid(row=1, column=1, sticky="w")
        tk.Spinbox(card, from_=3, to=15, textvariable=self.count, width=6, font=FONT,
                   state="readonly").grid(row=2, column=1, sticky="w")
        tk.Scale(card, from_=10, to=60, resolution=5, orient="horizontal", length=190, variable=self.seconds,
                 bg="white", highlightthickness=0).grid(row=3, column=1, sticky="w")
        for row, (text, var) in enumerate([("Shuffle questions and options", self.shuffle),
                                           ("Enable timer", self.timer_on)], start=4):
            tk.Checkbutton(card, text=text, variable=var, font=FONT, bg="white",
                           activebackground="white").grid(row=row, column=1, sticky="w")

        self.button(f, "START QUIZ", self.start_quiz)

    def start_quiz(self):
        if not self.name.get().strip():
            messagebox.showerror("Error", "Please enter your name.")
            return
        pool = list(QUESTIONS[self.category.get()])
        if self.shuffle.get():
            random.shuffle(pool)                                # shuffle question order
        self.questions = []
        for text, options, answer in pool[:int(self.count.get())]:
            if self.shuffle.get():                              # shuffle option order
                correct = options[answer]
                options = random.sample(options, len(options))
                answer = options.index(correct)
            self.questions.append((text, options, answer))
        self.index = self.score = 0
        self.answers = []
        self.show_question()

    # ---------------------------------------------------------- QUIZ
    def show_question(self):
        f = self.new_screen("quiz", f"Question {self.index + 1} of {len(self.questions)}   |   Score: {self.score}")
        question, options, _ = self.questions[self.index]
        self.choice.set(-1)

        if self.timer_on.get():
            self.time_left = self.seconds.get()
            self.bar = tk.Canvas(f, width=BAR, height=14, bg="#dddddd", highlightthickness=0)
            self.bar.pack(pady=(12, 0))
            self.rect = self.bar.create_rectangle(0, 0, BAR, 14, fill=GREEN, width=0)
            self.time_lbl = self.label("", 11, True)

        card = tk.Frame(f, **CARD)
        card.pack(fill="x", padx=40, pady=10)
        tk.Label(card, text=question, font=("Arial", 14, "bold"), wraplength=500, justify="left",
                 bg="white", padx=16, pady=14).pack(anchor="w")

        self.opts = []
        for i, text in enumerate(options):                      # Radiobuttons drawn as cards
            rb = tk.Radiobutton(f, text=f"   {'ABCD'[i]}.   {text}", variable=self.choice, value=i, indicatoron=0,
                                font=FONT, anchor="w", width=46, padx=10, pady=6, bd=0, bg="white",
                                selectcolor="#d9c8f5", highlightthickness=1, highlightbackground=BORDER,
                                cursor="hand2")
            rb.pack(pady=4)
            rb.bind("<Enter>", lambda e, w=rb: None if self.locked else w.config(bg=HOVER))   # mouse events
            rb.bind("<Leave>", lambda e, w=rb: None if self.locked else w.config(bg="white"))
            self.opts.append(rb)

        self.feedback = self.label(" ", 12, True)
        last = self.index == len(self.questions) - 1
        self.next_btn = self.button(f, "Finish" if last else "Next", self.next_question)
        if self.timer_on.get():
            self.tick()

    def tick(self):
        """Runs every second using after() so the window never freezes."""
        low = self.time_left <= self.seconds.get() * 0.25
        self.bar.coords(self.rect, 0, 0, BAR * self.time_left / self.seconds.get(), 14)
        self.bar.itemconfig(self.rect, fill=RED if low else GREEN)
        self.time_lbl.config(text=f"{self.time_left}s", fg=RED if low else "black")
        if self.time_left <= 0:
            self.next_question(timed_out=True)
        else:
            self.time_left -= 1
            self.job = self.root.after(1000, self.tick)

    def next_question(self, timed_out=False):
        if self.screen != "quiz" or self.locked:
            return
        picked = self.choice.get()
        if picked == -1 and not timed_out:
            messagebox.showwarning("Select an option", "Please choose an answer first.")
            return
        correct = self.questions[self.index][2]
        self.answers.append(picked)
        self.score += picked == correct
        self.locked = True
        self.cancel()

        for i, rb in enumerate(self.opts):                      # green = correct, red = wrong pick
            rb.config(state="disabled", disabledforeground="gray", bg="white")
            if i in (correct, picked):
                colour = GREEN if i == correct else RED
                rb.config(bg=colour, selectcolor=colour, disabledforeground="white")
        self.next_btn.config(state="disabled")
        self.feedback.config(text="Correct!" if picked == correct else "Time's up!" if picked == -1 else "Wrong!",
                             fg=GREEN if picked == correct else RED)
        self.job = self.root.after(1000, self.advance)

    def advance(self):
        self.index += 1
        self.show_question() if self.index < len(self.questions) else self.show_result()

    # ---------------------------------------------------------- RESULT
    def show_result(self):
        f = self.new_screen("result", "Quiz Completed!")
        total = len(self.questions)
        percent = self.score / total * 100
        self.label(f"{self.name.get().strip()}, you scored {self.score} / {total}  ({percent:.0f}%)", 14, True).pack_configure(pady=(20, 4))
        self.label("Excellent!" if percent >= 80 else "Good job, keep practising!" if percent >= 50
                   else "Keep learning, try again!", 13, True, GREEN if percent >= 50 else RED)

        c = tk.Canvas(f, width=220, height=190, bg=BG, highlightthickness=0)    # pie chart
        c.pack(pady=10)
        box = (30, 10, 190, 170)
        if self.score in (0, total):                            # a full 360-degree arc cannot be drawn
            c.create_oval(*box, fill=GREEN if self.score else RED, outline="")
        else:
            angle = 360 * self.score / total
            c.create_arc(*box, start=90, extent=angle, fill=GREEN, outline="")
            c.create_arc(*box, start=90 + angle, extent=360 - angle, fill=RED, outline="")
        for x, colour, name in ((35, GREEN, "Correct"), (120, RED, "Wrong")):   # legend
            c.create_rectangle(x, 179, x + 12, 191, fill=colour, outline="")
            c.create_text(x + 17, 185, text=name, anchor="w", font=("Arial", 10))

        row = tk.Frame(f, bg=BG)
        row.pack()
        for text, cmd, colour in (("Review Answers", self.show_review, PURPLE),
                                  ("Play Again", self.show_home, BLUE), ("Exit", self.quit_app, RED)):
            self.button(row, text, cmd, colour, "left")

    # ---------------------------------------------------------- REVIEW
    def show_review(self):
        f = self.new_screen("review", "Answer Review")
        self.button(f, "Back to Result", self.show_result, BLUE, "bottom")

        text = tk.Text(f, wrap="word", font=("Arial", 11), padx=10, pady=8, relief="flat")
        scroll = tk.Scrollbar(f, command=text.yview)
        text.config(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y", pady=10)
        text.pack(fill="both", expand=True, padx=(20, 0), pady=10)
        text.tag_config("good", foreground="green")
        text.tag_config("bad", foreground="red")

        for i, (question, options, answer) in enumerate(self.questions):
            picked = self.answers[i]
            mine = options[picked] if picked != -1 else "Not answered"
            text.insert("end", f"Q{i + 1}. {question}\nYour answer: {mine}\n", "good" if picked == answer else "bad")
            if picked != answer:
                text.insert("end", f"Correct answer: {options[answer]}\n", "good")
            text.insert("end", "\n")
        text.config(state="disabled")

    # ---------------------------------------------------------- EVENTS
    def on_enter(self, event):
        if self.screen == "quiz":
            self.next_question()
        elif self.screen == "home":
            self.start_quiz()

    def on_key(self, event):
        if self.screen == "quiz" and not self.locked and event.char.lower() in ("a", "b", "c", "d"):
            self.choice.set("abcd".index(event.char.lower()))


if __name__ == "__main__":
    root = tk.Tk()
    QuizApp(root)
    root.mainloop()