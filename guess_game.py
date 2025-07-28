import tkinter as tk
import random

# Generate random number
number_to_guess = random.randint(1, 100)
attempts = 0

def check_guess():
    global attempts
    guess = entry.get()
    if not guess.isdigit():
        result_label.config(text="Please enter a valid number!")
        return
    guess = int(guess)
    attempts += 1

    if guess > number_to_guess:
        result_label.config(text="Too High! Try again.")
    elif guess < number_to_guess:
        result_label.config(text="Too Low! Try again.")
    else:
        result_label.config(text=f"Congratulations! Guessed in {attempts} attempts.")

# GUI Setup
root = tk.Tk()
root.title("Guessing Game")
root.geometry("300x200")

title_label = tk.Label(root, text="Guess a number (1-100)", font=("Arial", 14))
title_label.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12))
entry.pack()

guess_button = tk.Button(root, text="Guess", command=check_guess, font=("Arial", 12))
guess_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack()

root.mainloop()
  
