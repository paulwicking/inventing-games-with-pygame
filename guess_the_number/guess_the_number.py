import random

MAX_VALUE = 20
MAX_GUESSES = 6
win_condition = False
number_of_guesses = 0

number_to_guess = random.randint(1, 20)

name = input('Hello! What is your name?\n')
print(f'Well, {name}, I am thinking of a number between 1 and {MAX_VALUE}.')

while not win_condition and number_of_guesses < MAX_GUESSES:  # using < to mimic range(6)
    try:
        current_guess = int(input('Take a guess.\n'))
    except ValueError:
        print('Please give me a number I can understand?')
        continue
    number_of_guesses += 1

    if current_guess == number_to_guess:
        win_condition = True
        break
    elif current_guess > number_to_guess:
        print('Your guess is too high.')
    elif current_guess < number_to_guess:
        print('Your guess is too low.')

if win_condition:
    print(f'Good job, {name}! You guessed my number in {number_of_guesses} guesses!')
else:
    print(f'Too bad! I was thinking about {number_to_guess}')

