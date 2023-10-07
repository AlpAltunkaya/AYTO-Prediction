from tqdm import tqdm  # Import the tqdm library for progress bars
import itertools
import pandas as pd

# Men and Women lists based on your provided data
men = ['Danilo', 'Elia', 'Emanuell', 'Fabio', 'Marvin', 'Max', 'Mike', 'Paco', 'Steffen', 'Teezy']
women = ['Alicia', 'Darya', 'Jennifer', 'Kim', 'Marie', 'Paulina', 'Sabrina', 'Sandra', 'Shakira', 'Steffi']


# List of every week's guesses based on the provided data
allWeeks = [
    ([('Danilo', 'Darya'), ('Paco', 'Sandra'), ('Steffen', 'Paulina'), ('Marvin', 'Shakira'), ('Mike', 'Kim'), ('Emanuell', 'Sabrina'), ('Elia', 'Jennifer'), ('Fabio', 'Marie'), ('Teezy', 'Steffi'), ('Max', 'Alicia')], 3),
    ([('Mike', 'Sabrina'), ('Danilo', 'Paulina'), ('Paco', 'Kim'), ('Steffen', 'Alicia'), ('Marvin', 'Jennifer'), ('Teezy', 'Steffi'), ('Emanuell', 'Darya'), ('Fabio', 'Marie'), ('Max', 'Shakira'), ('Elia', 'Sandra')], 2),
    ([('Steffen', 'Alicia'), ('Max', 'Sabrina'), ('Paco', 'Sandra'), ('Fabio', 'Shakira'), ('Elia', 'Marie'), ('Danilo', 'Darya'), ('Marvin', 'Steffi'), ('Mike', 'Paulina'), ('Teezy', 'Kim'), ('Emanuell', 'Jennifer')], 2),
    ([('Steffen', 'Sandra'), ('Max', 'Paulina'), ('Elia', 'Marie'), ('Danilo', 'Darya'), ('Fabio', 'Shakira'), ('Paco', 'Sabrina'), ('Peter', 'Kim'), ('Emanuell', 'Steffi'), ('Marvin', 'Jennifer'), ('Teezy', 'Alicia')], 4),
    ([('Emanuell', 'Sabrina'), ('Paco', 'Shakira'), ('Mike', 'Paulina'), ('Teezy', 'Kim'), ('Marvin', 'Jennifer'), ('Max', 'Sandra'), ('Steffen', 'Alicia'), ('Fabio', 'Marie'), ('Elia', 'Steffi'), ('Danilo', 'Darya')], 3),
    ([('Paco', 'Alicia'), ('Steffen', 'Sandra'), ('Mike', 'Paulina'), ('Marvin', 'Jennifer'), ('Fabio', 'Shakira'), ('Elia', 'Marie'), ('Max', 'Sabrina'), ('Emanuell', 'Steffi'), ('Teezy', 'Kim'), ('Danilo', 'Darya')], 4),
    ([('Fabio', 'Alicia'), ('Paco', 'Jennifer'), ('Teezy', 'Kim'), ('Steffen', 'Marie'), ('Marvin', 'Paulina'), ('Emanuell', 'Sabrina'), ('Mike', 'Sandra'), ('Max', 'Shakira'), ('Elia', 'Steffi'), ('Danilo', 'Darya')], 3)
]

# The matches that got denied in the Truth Booth
truthBooth_denied = [('Danilo', 'Jennifer'), ('Elia', 'Jennifer'), ('Mike', 'Kim'), ('Teezy', 'Alicia')]

# Function to determine the number of matches between two lists of couples
def correlation(list1, list2):
    total = 0
    for couple in list1:
        if couple in list2:
            total += 1
    return total

# Function to check if a list of matches is impossible based on known information
def isImpossible(matchlist):
    for match in truthBooth_denied:
        if match in matchlist:
            return True
    for week in allWeeks:
        if correlation(matchlist, week[0]) != week[1]:
            return True
    return False

# List to store all possible matches
possible = []

# Generate all possible matches using permutations
iterable = itertools.permutations(women, len(men))
import math

total_iterations = math.factorial(len(women))

# Wrap the iterable with tqdm for a progress bar
for matching in tqdm(iterable, total=total_iterations):
    matchlist = list(zip(men, matching))
    if isImpossible(matchlist):
        continue
    else:
        possible.append(matchlist)

# Flatten the list of possible matchings
flattened_possible = [match for sublist in possible for match in sublist]

# Create a DataFrame
df = pd.DataFrame(flattened_possible, columns=['Men', 'Women'])

# Display the DataFrame to see the table
print(df)
