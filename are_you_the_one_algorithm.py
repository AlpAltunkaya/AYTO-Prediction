# Importing required modules
import itertools
import pickle

# The list of men and women as provided
men = ['Danilo', 'Elia', 'Emanuell', 'Fabio', 'Marvin', 'Max', 'Mike', 'Paco', 'Steffen', 'Teezy']
women = ['Alicia', 'Darya', 'Jennifer', 'Kim', 'Marie', 'Paulina', 'Sabrina', 'Sandra', 'Shakira', 'Steffi']

# Truth Booth results
truthBooth_confirmed = [("Danilo", "Darya")]
truthBooth_denied = [("Danilo", "Jennifer"), ("Elia", "Jennifer"), ("Mike", "Kim"), ("Teezy", "Alicia")]

# Function to check if a match list is impossible based on Truth Booth results and observed lit lights
def isImpossible(matchlist, allWeeks, truthBooth_denied, truthBooth_confirmed):
    for match in truthBooth_denied:
        if match in matchlist:
            return True
    for match in truthBooth_confirmed:
        if match not in matchlist:
            return True
    for week in allWeeks:
        if sum([1 for match in matchlist if match in week[0]]) != week[1]:
            return True
    return False

# Generate all possible combinations instead of permutations, as order is not important
possible = []

# Generate all possible match combinations
for matching in itertools.product(men, repeat=len(women)):
    # Create a list of tuples representing the matches
    matchlist = [(men[i], women[j]) for i, j in enumerate(matching)]
    
    # Each woman should appear exactly once in the match list for it to be valid
    if len(set(matching)) != len(women):
        continue
    
    # Skip match lists that are impossible based on the given constraints
    if isImpossible(matchlist, allWeeks, truthBooth_denied, truthBooth_confirmed):
        continue
    
    possible.append(matchlist)

# Create a dictionary to hold the match likelihoods
match_dictionary = {}
for man in men:
    for woman in women:
        match_dictionary[(man, woman)] = 0

# Calculate the likelihood of each match
for matchlist in possible:
    for match in matchlist:
        match_dictionary[match] += 1 / len(possible)

# Convert likelihoods to percentages
for key in match_dictionary.keys():
    match_dictionary[key] *= 100

len(possible), match_dictionary