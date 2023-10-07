#Trigger warning: Sexism
#To make the code correctly identify possible couples, man's name
#needs to be written first, followed by the woman's name.


from tqdm import tqdm  # Import the tqdm library for progress bars
import itertools
import pandas as pd

# Men and Women lists based on the fictional cast
men = ['Adam', 'Bob', 'Charlie', 'David', 'Eddie']
women = ['Fiona', 'Grace', 'Hannah', 'Isabel', 'Jenny']

# List of every week's guesses based on the fictional data
allWeeks = [
    ([('Charlie', 'Isabel'), ('Eddie', 'Hannah'), ('David', 'Jenny'), ('Adam', 'Fiona'), ('Bob', 'Grace')], 2),
    ([('Adam', 'Grace'), ('Charlie', 'Hannah'), ('David', 'Fiona'), ('Bob', 'Jenny'), ('Eddie', 'Isabel')], 1),
    ([('Adam', 'Hannah'), ('Bob', 'Grace'), ('David', 'Jenny'), ('Eddie', 'Fiona'), ('Charlie', 'Isabel')], 1),
    ([('Charlie', 'Jenny'), ('David', 'Fiona'), ('Eddie', 'Hannah'), ('Bob', 'Isabel'), ('Adam', 'Grace')], 0),
    ([('Charlie', 'Hannah'), ('Adam', 'Fiona'), ('Bob', 'Isabel'), ('David', 'Grace'), ('Eddie', 'Jenny')], 3)
]

# The matches that got denied in the Truth Booth
truthBooth_denied = [('Adam', 'Hannah'), ('Charlie', 'Isabel')]

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
