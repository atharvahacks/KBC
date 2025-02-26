import time
import random
import threading

# Questions which are fixed
questions = [
    ["1. What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], "C"],
    ["2. Who wrote the play Romeo and Juliet?", ["Charles Dickens", "William Shakespeare", "Mark Twain", "J.K. Rowling"], "B"],
    ["3. What is the chemical symbol for water?", ["O₂", "CO₂", "H₂O", "HO₂"], "C"],
    ["4. Who wrote the Indian national anthem?", ["Rabindranath Tagore", "Bankim Chandra Chatterjee", "Subramania Bharati", "Sarojini Naidu"], "A"],
    ["5. Who was the first President of the United States?", ["Abraham Lincoln", "Thomas Jefferson", "John Adams", "George Washington"], "D"],
    ["6. What is the hardest natural substance on Earth?", ["Diamond", "Iron", "Steel", "Quartz"], "A"],
    ["7. Which country has the largest population in the world as of 2024?", ["China", "India", "USA", "Russia"], "B"],
    ["8. Who was the first Indian to travel in space?", ["Kalpana Chawla", "Rakesh Sharma", "Sunita Williams", "Vikram Sarabhai"], "B"],
    ["9. Which element has the highest melting point?", ["Tungsten (W)", "Platinum (Pt)", "Carbon (C)", "Iron (Fe)"], "A"],
    ["10. Which country won the FIFA World Cup in 2018?", ["Brazil", "Germany", "France", "Argentina"], "C"],
    ["11. Which ocean is the deepest in the world?", ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"], "C"],
    ["12. Which African country was never colonized?", ["Kenya", "Nigeria", "Ethiopia", "South Africa"], "C"],
    ["13. Which ancient civilization built the Machu Picchu?", ["Incas", "Aztecs", "Mayans", "Egyptians"], "A"],
    ["14. What is the name of the only non-metal that exists in a liquid state at room temperature?", ["Mercury", "Bromine", "Chlorine", "Phosphorus"], "B"],
    ["15. Which famous mathematical problem was solved by Andrew Wiles in 1994?", ["Riemann Hypothesis","P vs NP Problem","Fermat’s Last Theorem","Goldbach’s Conjecture"],"C"],
    ["16. What is the longest known word in English, which refers to a lung disease caused by inhaling silica dust?", ["Hippopotomonstrosesquippedaliophobia","Floccinaucinihilipilification","Pneumonoultramicroscopicsilicovolcanoconiosis","Antidisestablishmentarianism"],"C"]
]

# Introduction
name = input("Aapka naam jaan sakte hai: ")
print(f"\nSwagat hai aapka {name} ji Kaun Banega Crorepati me!!!")
print("\nAapse 16 prashna puche jaynege jinke sahi jawab dene par aap utni hi dhanrashi kamayiega!")
print("\nAapke khel me 2 padav hai: pehla padav 10,000 rupaye aur doosra padav 3,20,000 rupaye")
print("\nPehle 5 prashno ke liye aapko milege 45 second, aur 6-10 prashno ke liye 60 second!")
print("\nAap agar chahe to khel ko kabhi bhi 'QUIT' likh kar band kar sakte hai!")
print("\nTo shuru karte hai Kaun Banega Crorepati!")
print("\nPress Enter to start the game....")
input()

# Initialized the price and money for each right question
price = [1000, 2000, 3000, 5000, 10000, 20000, 40000, 80000, 160000, 320000, 640000, 1250000, 2500000, 5000000, 10000000, 70000000]

money = 0

guaranteed_prize = 0

# Expert name and details
expert_name = "Atharva Degwekar"

expert_details = "He is an Engineer aur apne research ke liye bahut prasiddh hai, aur duniya ke shreshth engineers mein se ek hai."

# Lifelines dictionary remains unchanged
lifelines = {
    "50-50": True,
    "Audience-Poll": True,
    "Expert-Advice": True
}

# Timer functionality: a function that takes timeout_duration in seconds
def get_answer_with_timer(timeout_duration):
    global user_answer
    user_answer = None

    def input_thread():
        global user_answer
        user_answer = input("\nAapka jawab: ").strip().upper()

    thread = threading.Thread(target=input_thread)
    thread.start()
    thread.join(timeout=timeout_duration)

    if thread.is_alive():
        print("\n⏳ Samay samapt ho gaya! Aap jawab nahi de paaye! 😞")
        user_answer = "QUIT"

# Lifeline Functions (unchanged)
def use_5050(question, options, correct_answer):
    wrong_answers = [opt for idx, opt in enumerate(["A", "B", "C", "D"]) if opt != correct_answer]
    random.shuffle(wrong_answers)
    removed = wrong_answers[:2]
    print("Computer Mahashay 50-50 ko ankit kiya jaye")
    print("50-50 ke baad aapke options hai:")
    print(question)
    for i, option in enumerate(options):

        if ["A", "B", "C", "D"][i] in removed:
            print(f"{['A', 'B', 'C', 'D'][i]}. ---")

        else:
            print(f"{['A', 'B', 'C', 'D'][i]}. {option}")

def use_Audience(correct_answer):
    votes = {"A": random.randint(5, 25), "B": random.randint(5, 25), "C": random.randint(5, 25), "D": random.randint(5, 25)}
    votes[correct_answer] = random.randint(40, 70)
    total = sum(votes.values())
    for key in votes:
        votes[key] = round(votes[key] / total * 100, 1)
    print("Computer Mahashay Audience-Poll ko ankit kiya jaye")
    print("\nDekhte hai audience ka kya kehna hai:")

    for opt in ["A", "B", "C", "D"]:
        print(f"{opt}: {votes[opt]}%")

def use_Expert(correct_answer):
    print("Computer Mahashay Expert-Advice lifeline ko ankit kiya jaye")
    if random.random() < 0.8:
        print(f"\nExpert Advice: Main 80% sure hu ki answer hai: {correct_answer}.")

    else:
        options = ["A", "B", "C", "D"]
        options.remove(correct_answer)
        print(f"\nExpert Advice: Main sure to nahi hu, par mujhe lagta hai iska uttar ye ho sakta hai: {random.choice(options)}.")

# Main game loop
for i in range(len(questions)):
    question, options, correct_answer = questions[i]
    print(f"\n{i+1} sawal {price[i]} rupayo ke liye aapke screen ke uppar ye raha!!")
    print(f"\n{question}")
    print(f"a. {options[0]}                    b. {options[1]}")
    print(f"c. {options[2]}                    d. {options[3]}")

    # Timer logic based on question number:
    # For first 5 questions (i=0 to 4): 45 seconds timer
    # For questions 6-10 (i=5 to 9): 60 seconds timer
    # For questions 11 onward: no timer (or you can set a timer if needed)
    if i < 5:
        get_answer_with_timer(45)

    elif i < 10:
        get_answer_with_timer(60)

    else:
        user_answer = input("\nAapka jawab: ").strip().upper()

    # Lifeline handling and answer input:
    while user_answer not in ["A", "B", "C", "D", "QUIT"]:

        # If user enters a lifeline command instead
        if user_answer == "50-50" and lifelines["50-50"]:
            print(f"\n{name} ji, aap 50-50 lifeline ka istemal kar rahe hai.")
            use_5050(question, options, correct_answer)
            lifelines["50-50"] = False

        elif user_answer == "AUDIENCE-POLL" and lifelines["Audience-Poll"]:
            print(f"\n{name} ji, aap Audience-Poll lifeline ka istemal kar rahe hai.")
            use_Audience(correct_answer)
            lifelines["Audience-Poll"] = False

        elif user_answer == "EXPERT-ADVICE" and lifelines["Expert-Advice"]:
            print(f"\n{name} ji, aap Expert-Advice lifeline ka istemal kar rahe hai.")
            use_Expert(correct_answer)
            lifelines["Expert-Advice"] = False

        else:
            print("Mahoday, kripya diye gaye options me se chuniye: A, B, C, ya D (ya lifeline command).")

        # Get the answer again (without timer for lifeline re-entry)
        user_answer = input("\nAapka jawab: ").strip().upper()

    # Quit condition
    if user_answer == "QUIT":
        print(f"\nAapne khel chhod diya! Aap jeet gaye ₹{money} rupaye!")
        break

    # Check answer correctness
    if user_answer == correct_answer:
        money = price[i]
        print(f"\n Sahi jawab Aapka aap ₹{money} jeet chuke hai!")

    else:
        print(f"\n Galat jawab! Sahi jawab tha: {correct_answer}.")
        print(f"\nAap jeet gaye ₹{guaranteed_prize} rupaye!")
        break

    # Set guaranteed prize milestones:
    if money >= 10000:
        print("\nMubarak ho! Aap pehla padav ₹10,000 tak pahunch chuke hain. Ab aap isse nischit taur par ghar le jayiyega.")
        guaranteed_prize = 10000

    if money >= 320000:
        print("\nMubarak ho! Aap ₹3,20,000 padav tak pahunch gaye hain. Ab aap isse kam nahi jeetenge!!")
        guaranteed_prize = 320000

print(f"\nBHOT BHOT DHANYADWAD! Aapne jeet liye ₹{money} rupaye!")

print(f"\n to abhi hamare samne the{name}. aur vo yaha se jeet kar gaye hai ₹{money}!")

def wish():
    timestamp = time.strftime('%H:%M:%S')
    print(timestamp)

# wishing logic
    if timestamp > "12:00:00":
        print("Shubh dupehr!")
        print("Have a nice afternoon")

    elif timestamp > "16:00:00":
        print("Shubh Sandhya!")
        print("Have a nice evening!!")

    elif timestamp > "20:00:00":
        print("Shubh Ratri! Shubh Ratri! Shubh Ratri!")
        print("Khud ki aur parivar ke swasthya ka dhyan rakhe")

    elif timestamp > "5:00:00":
        print("Good morning!!")
        print("Aapka din managalmay ho")

    else:
        print("BHOT BHOT AABHAR AAPKE AUR PHIR MILENGE KAUN BANEGA CROREPATI ME!")
# calling the wishing logic
wish()

# End of the code
print("BHOT BHOT AABHAR AAPKE AUR PHIR MILENGE KAUN BANEGA CROREPATI ME!")