import tkinter as tk
from tkinter import messagebox
import random
import requests

# Function to fetch questions from an online source
def fetch_questions():
    try:
        response = requests.get('https://opentdb.com/api.php?amount=10&type=multiple')
        data = response.json()
        questions = []
        for item in data['results']:
            question = item['question']
            correct_answer = item['correct_answer']
            incorrect_answers = item['incorrect_answers']
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)
            questions.append((question, options, correct_answer))
        return questions
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch questions: {e}")
        return []

# Fetch questions
questions = fetch_questions()

# Lifelines (each can be used once)
lifelines = {"50-50": True, "Ask the Audience": True, "Phone a Friend": True}

# Game state variables
current_question = 0
total_prize = 0
prize_money = [1000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 3000000, 5000000, 10000000, 50000000, 70000000]

# GUI setup
root = tk.Tk()
root.title("KBC - Kaun Banega Crorepati")
root.geometry("600x500")
root.configure(bg='black')

# UI Elements
question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=580, bg='blue', fg='white')
question_label.pack(pady=20)

# Buttons and functions
buttons = []
button_colors = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 12), width=25, bg=button_colors[i], fg='white', command=lambda i=i: check_answer(i))
    btn.pack(pady=5)
    buttons.append(btn)

# Prize Money
prize_label = tk.Label(root, text="Prize Money: ₹0", font=("Arial", 12, "bold"), bg='black', fg='white')
prize_label.pack(pady=10)

# Lifeline Buttons
lifeline_frame = tk.Frame(root, bg='black')
lifeline_frame.pack(pady=10)

# Lifeline Buttons
lifeline_buttons = {
    "50-50": tk.Button(lifeline_frame, text="🎭 50-50", bg='#9C27B0', fg='white', command=lambda: use_lifeline("50-50")),
    "Ask the Audience": tk.Button(lifeline_frame, text="📊 Ask the Audience", bg='#FFEB3B', fg='black', command=lambda: use_lifeline("Ask the Audience")),
    "Phone a Friend": tk.Button(lifeline_frame, text="📞 Phone a Friend", bg='#00BCD4', fg='white', command=lambda: use_lifeline("Phone a Friend"))
}

for btn in lifeline_buttons.values():
    btn.pack(side=tk.LEFT, padx=5)

# Function to Load Next Question
def load_question():
    global current_question
    if current_question < len(questions):
        q, opts, _ = questions[current_question]
        question_label.config(text=f"Q{current_question+1}: {q} (₹{prize_money[current_question]})")
        for i in range(4):
            buttons[i].config(text=opts[i], state=tk.NORMAL, bg=button_colors[i])
    else:
        messagebox.showinfo("Game Over", f"🎉 You won ₹{total_prize}! Thanks for playing!")
        root.quit()

# Function to Check Answer
def check_answer(choice):
    global current_question, total_prize
    _, opts, correct_answer = questions[current_question]

    if opts[choice] == correct_answer:
        total_prize = prize_money[current_question]
        prize_label.config(text=f"Prize Money: ₹{total_prize}")
        current_question += 1
        load_question()
    else:
        messagebox.showinfo("Game Over", f"❌ Wrong answer! The correct answer was: {correct_answer}\n🏆 You won ₹{total_prize}!")
        root.quit()

# Lifeline Functions
def use_lifeline(lifeline):
    global lifelines
    if not lifelines[lifeline]:
        messagebox.showinfo("Lifeline Used", f"You have already used {lifeline}.")
        return

    q, opts, correct_answer = questions[current_question]

    if lifeline == "50-50":
        incorrect_options = [opt for opt in opts if opt != correct_answer]
        random.shuffle(incorrect_options)
        remove_options = incorrect_options[:2]

        for btn in buttons:
            if btn["text"] in remove_options:
                btn.config(state=tk.DISABLED)

    elif lifeline == "Ask the Audience":
        probabilities = [random.randint(10, 50) for _ in range(4)]
        correct_index = opts.index(correct_answer)
        probabilities[correct_index] = max(50, random.randint(50, 80))  # Ensuring higher probability for the correct answer

        audience_result = "\n".join([f"{opts[i]}: {probabilities[i]}%" for i in range(4)])
        messagebox.showinfo("📊 Audience Poll", audience_result)

    elif lifeline == "Phone a Friend":
        hints = [
            f"I think the answer is {correct_answer}.",
            f"Not sure, but {correct_answer} seems right.",
            f"I'm 70% sure it's {correct_answer}.",
            f"I heard once that {correct_answer} is the right answer!"
        ]
        messagebox.showinfo("📞 Phone a Friend", random.choice(hints))

    lifelines[lifeline] = False  # Mark the lifeline as used
    lifeline_buttons[lifeline].config(state=tk.DISABLED)

# Start Game
load_question()
root.mainloop()
