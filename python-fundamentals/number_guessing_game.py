import random


def show_score(attempts_list):
    if not attempts_list:
        print("There is currently no be st score, it's yours for the taking!")
    else:
        print(f"The current best score is {min(attempts_list)} attempts.")


def start_game():
    attempts = 0 # Track the number of attempts in the current game
    rand_num = random.randint(1, 10) # Generates a random number
    attempts_list = [] # Stores past attempts for tracking the best score

    print("Hello, traveler! Welcome to game of guesses!")
    player_name = input("What is your name? ") # Gets the player's name

    wanna_play = input(f"Hi, {player_name}, would you like to play the guessing game? (Enter Yes/No): ")
    
    if wanna_play.lower() != "yes":
        print("That's cool, Thanks!")
        exit()
    else:
        show_score(attempts_list) # Show the best score before starting
    

    # Game loop
    while wanna_play.lower() == "yes":
        try:
            guess = int(input("Pick a number between 1 and 10: ")) # Get user input

            if guess < 1 or guess > 10:
                raise ValueError("Please guess a number within the given range")

            attempts += 1 # Count each guess

            if guess == rand_num:
                print("Nice! You got it! 🎉")
                print(f"It took you {attempts} attempts.")

                attempts_list.append(attempts) # Save the attempt count
                wanna_play = input("Would you like to play again? (Enter Yes/No): ")

                if wanna_play.lower() != "yes":
                    print("That's cool, have a good one!")
                    break
                else:
                    attempts = 0 # Reset attempts for the new game
                    rand_num = random.randint(1, 10) # Pick a new number
                    show_score(attempts_list) # Show the best score
                    continue
            else:
                # Provide hints
                if guess > rand_num:
                    print("It's lower! 📉")
                elif guess < rand_num:
                    print("It's higher! 📈")
        
        except ValueError as err:
            print("Oh no! That is not a valid numer. Try again...")
            print(err) # Show error message

if __name__ == "__main__":
    start_game()