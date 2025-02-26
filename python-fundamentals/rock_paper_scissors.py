"""
This script implements a simple Rock, Paper, Scissors game that can be played in the terminal.
Functions:
    clear(): Clears the terminal screen.
    main(): The main function that runs the Rock, Paper, Scissors game.
The game allows a user to play against the computer. The first to win 3 rounds is declared the winner.
"""

import random
import os


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    print("Welcome to Rock 🪨, Paper 📄, or Scissors ✂️")
    name = input("What's your name?: ")
    print(f"Hello {name}, let's play 🕹️\n")

    options = ["rock", "paper", "scissors"]
    round = 1
    wins = 0
    losses = 0

    while wins < 3 and losses < 3:
        print("Choose an option:")
        print("1. Rock 🪨")
        print("2. Paper 📄")
        print("3. Scissors ✂️\n")

        choice = input("What do you choose?: ")

        if choice == "1":
            clear()
            print("You chose 'rock' 🪨\n")
            player = "rock"
        elif choice == "2":
            clear()
            print("You chose 'paper' 📄\n")
            player = "paper"
        elif choice == "3":
            clear()
            print("You chose 'scissors' ✂️\n")
            player = "scissors"
        else:
            clear()
            print("Invalid option ❌\n")
            continue

        computer = random.choice(options)
        print(f"The computer chose '{computer}'\n")

        if player == computer:
            print("It's a tie 🤝")
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            print("You won 🎉")
            wins += 1
        else:
            print("You lost 😢")
            losses += 1
   
        print(f"Round {round}: {name} 🧒 {wins} vs Computer 💻 {losses}\n")
        round += 1
    
    if wins == 3:
        print("Congratulations 🎉, you won!")
    else:
        print("Sorry 😢, you lost!")


if __name__ == "__main__":
    main()