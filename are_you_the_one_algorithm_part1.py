
import itertools
import pickle
from itertools import combinations

# Specifies whether the matches should be loaded from the match file
# For the first few times you run, make sure this is set to False.
# Then you can change it to True in order to run faster.
load_from_file = False

# Guys and girls based on the provided list
men = ['Danilo', 'Elia', 'Emanuell', 'Fabio', 'Marvin', 'Max', 'Mike', 'Paco', 'Steffen', 'Teezy']
women = ['Alicia', 'Darya', 'Jennifer', 'Kim', 'Marie', 'Paulina', 'Sabrina', 'Sandra', 'Shakira', 'Steffi']

# List of every week's guesses based on the Excel sheet
allWeeks = [
    ([('Darya', 'Danilo'), ('Sandra', 'Paco'), ('Paulina', 'Steffen'), ('Shakira', 'Marvin'), ('Kim', 'Mike'), ('Sabrina', 'Emanuell'), ('Jennifer', 'Elia'), ('Marie', 'Fabio'), ('Steffi', 'Teezy'), ('Alicia', 'Max')], 3),
    ([('Mike', 'Sabrina'), ('Danilo', 'Paulina'), ('Paco', 'Kim'), ('Steffen', 'Alicia'), ('Marvin', 'Jennifer'), ('Teezy', 'Steffi'), ('Emanuell', 'Darya'), ('Fabio', 'Marie'), ('Max', 'Shakira'), ('Elia', 'Sandra')], 2),
    ([('Alicia', 'Steffen'), ('Sabrina', 'Max'), ('Sandra', 'Paco'), ('Shakira', 'Fabio'), ('Marie', 'Elia'), ('Darya', 'Danilo'), ('Steffi', 'Marvin'), ('Paulina', 'Mike'), ('Kim', 'Teezy'), ('Jennifer', 'Emanuell')], 2),
    ([('Steffen', 'Sandra'), ('Max', 'Paulina'), ('Elia', 'Marie'), ('Danilo', 'Darya'), ('Fabio', 'Shakira'), ('Paco', 'Sabrina'), ('Max', 'Kim'), ('Emanuell', 'Steffi'), ('Marvin', 'Jennifer'), ('Teezy', 'Alicia')], 4),
    ([('Emanuell', 'Sabrina'), ('Paco', 'Shakira'), ('Mike', 'Paulina'), ('Teezy', 'Kim'), ('Marvin', 'Jennifer'), ('Max', 'Sandra'), ('Steffen', 'Alicia'), ('Fabio', 'Marie'), ('Elia', 'Steffi'), ('Danilo', 'Darya')], 3),
    ([('Paco', 'Alicia'), ('Steffen', 'Sandra'), ('Mike', 'Paulina'), ('Marvin', 'Jennifer'), ('Fabio', 'Shakira'), ('Elia', 'Marie'), ('Max', 'Sabrina'), ('Emanuell', 'Steffi'), ('Teezy', 'Kim'), ('Danilo', 'Darya')], 4),
    ([('Alicia', 'Fabio'), ('Jennifer', 'Paco'), ('Kim', 'Teezy'), ('Marie', 'Steffen'), ('Paulina', 'Marvin'), ('Sabrina', 'Emanuell'), ('Sandra', 'Mike'), ('Shakira', 'Max'), ('Steffi', 'Elia'), ('Danilo', 'Darya')], 3)
]
# The matches that got denied in the Truth Booth
truthBooth_denied = [('Danilo', 'Jennifer'), ('Elia', 'Jennifer'), ('Mike', 'Kim'), ('Teezy', 'Alicia')]

# The matches that were confirmed in the Truth Booth
truthBooth_confirmed = [('Danilo', 'Darya')]

# Helper functions and main algorithm remain the same as in the original code,
# but with adaptations to use combinations instead of permutations, and to use the preprocessed data.

# Returns the number of matches in common between two match lists
def correlation(list1, list2):
    total = 0
    for couple in list1:
        if couple in list2:
            total += 1
    return total

# Returns whether a matchlist breaks a rule
def isImpossible(matchlist):
    for match in truthBooth_denied:
        if match in matchlist:
            return True
    for match in truthBooth_confirmed:
        if match not in matchlist:
            return True
    for week in allWeeks:
        if correlation(matchlist, week[0]) != week[1]:
            return True        
    return False

# List of possible matches
possible = []

# Generate all possible matches using permutations
iterable = combinations(women, len(women))  # We need permutations here because the men and women lists are distinct
for matching in iterable:
    matchlist = list(zip(men, matching))  # Create tuples for each match
    # Skip match lists that break a rule
    if isImpossible(matchlist):
        continue
    else:
        possible.append(matchlist)

# Initialize dictionary to hold match probabilities
match_dictionary = {}
for guy in men:
    match_dictionary[guy] = [0] * len(women)

# Calculate probabilities
for matching in possible:
    for guy in men:
        match_dictionary[guy][women.index(matching[men.index(guy)])] += float(1)/len(possible)

# The rest of the code can include calculations and visualizations based on match_dictionary,
# such as finding the most likely matches, plotting the probabilities, etc.

# Save the possible matches into a file for future use
pickle.dump(possible, open("allmatches.p", "wb"))
