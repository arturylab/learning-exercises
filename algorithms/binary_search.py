"""
This script implements a binary search algorithm to guess a number that the user is thinking of within a specified range.
"""


def binary_search(lower=1, upper=100):
    """
    Performs a binary search to guess a number between a specified range.

    The function prompts the user to think of a number within the given range and then attempts to guess the number using a binary search algorithm. The user provides feedback on whether the guessed number is too high, too low, or correct.

    Args:
        lower (int, optional): The lower bound of the range. Defaults to 1.
        upper (int, optional): The upper bound of the range. Defaults to 100.

    The algorithm works by repeatedly dividing the search interval in half. If the guess is too high, the upper bound is adjusted. If the guess is too low, the lower bound is adjusted. This process continues until the correct number is guessed.

    Returns:
        None
    """
    int(input(f"Guess a number between {lower} and {upper}: "))
    attempts = 0

    while lower <= upper:
        mid = (lower + upper) // 2
        attempts += 1
        print(f"\n🔍 Attempt {attempts}: Is the number {mid}?")

        response = input("Enter 'l' for lower ⬇️, 'h' for higher ⬆️, 'y' for yes ✅: ").strip().lower()

        if response == 'y':
            print(f"\n🎉 Congratulations! The number is {mid}")
            print(f"📈 Number of attempts: {attempts}")
            return
        elif response == 'l':
            upper = mid - 1
        elif response == 'h':
            lower = mid + 1
        else:
            print("❌ Invalid input. Please enter 'l' for lower ⬇️, 'h' for higher ⬆️, 'y' for yes ✅")


if __name__ == "__main__":
    binary_search()
