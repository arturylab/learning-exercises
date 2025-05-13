import random

# Ask the user for their name and greet them
name = input("What is your name? ")
print(f"Hello, {name}! Welcome to the word guessing game!")

# List of possible words (programming, math, and science terms)
words = [
    # Programming languages
    "python", "java", "javascript", "ruby", "html", "css", "c", "csharp", "cpp", "go", "rust", "swift", "kotlin", "typescript", "php", "perl", "scala", "haskell", "matlab", "r", "dart", "objectivec", "lua", "bash", "fortran",
    # Math terms
    "algebra", "geometry", "calculus", "matrix", "vector", "integral", "derivative", "equation", "theorem", "proof", "function", "variable", "logarithm", "fraction", "integer", "prime", "factorial", "polynomial", "sequence", "series",
    # Science terms
    "physics", "chemistry", "biology", "atom", "molecule", "cell", "energy", "force", "gravity", "electron", "proton", "neutron", "element", "compound", "reaction", "evolution", "ecosystem", "photosynthesis", "genetics", "organism", "bacteria",
    # More programming and tech
    "algorithm", "database", "array", "loop", "recursion", "object", "class", "inheritance", "interface", "module", "package", "syntax", "compiler", "interpreter", "debugger", "variable", "constant", "pointer", "reference", "stack",
    # More math and science
    "statistics", "probability", "geometry", "trigonometry", "angle", "radius", "diameter", "circumference", "hypotenuse", "vector", "scalar", "momentum", "velocity", "acceleration", "mass", "density", "pressure", "temperature", "solution", "mixture"
]

# Randomly select a word from the list
word = random.choice(words)

print("Guess the word! It can be a programming language, math term, or science term.")
print("You have 6 attempts to guess the word.")

guesses = ''  # Store the letters guessed by the user
attempts = 6  # Number of attempts allowed

# Main game loop
while attempts > 0:
    failed = 0  # Counter for unguessed letters

    # Display the word with guessed letters revealed
    for char in word:
        if char in guesses:
            print(char, end=' ')
        else:
            print("_", end=' ')
            failed += 1

    print()

    # If all letters have been guessed, the user wins
    if failed == 0:
        print("Congratulations! You've guessed the word!")
        break

    # Ask the user to guess a letter
    guess = input("Guess a character: ").lower()
    guesses += guess

    # If the guessed letter is not in the word, decrement attempts
    if guess not in word:
        attempts -= 1
        print(f"Wrong guess! You have {attempts} attempts left.")
        # If no attempts are left, the user loses
        if attempts == 0:
            print(f"Sorry, you've run out of attempts. The word was '{word}'.")