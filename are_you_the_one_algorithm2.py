
import itertools
import pickle

# Configurations
load_from_file = False

# Contestants
men = ['Danilo', 'Elia', 'Emanuell', 'Fabio', 'Marvin', 'Max', 'Mike', 'Paco', 'Steffen', 'Teezy']
women = ['Alicia', 'Darya', 'Jennifer', 'Kim', 'Marie', 'Paulina', 'Sabrina', 'Sandra', 'Shakira', 'Steffi']

# Matching nights and truth booths
allWeeks = [(['Darya', 'Sandra', 'Paulina', 'Shakira', 'Kim', 'Sabrina', 'Jennifer', 'Marie', 'Steffi', 'Alicia'], 3), (['Sabrina', 'Paulina', 'Kim', 'Alicia', 'Jennifer', 'Steffi', 'Darya', 'Marie', 'Shakira', 'Sandra'], 2), (['Alicia', 'Sabrina', 'Sandra', 'Shakira', 'Marie', 'Darya', 'Steffi', 'Paulina', 'Kim', 'Jennifer'], 2), (['Sandra', 'Paulina', 'Marie', 'Darya', 'Shakira', 'Sabrina', 'Kim', 'Steffi', 'Jennifer', 'Alicia'], 4), (['Sabrina', 'Shakira', 'Paulina', 'Kim', 'Jennifer', 'Sandra', 'Alicia', 'Marie', 'Steffi', 'Darya'], 3), (['Alicia', 'Sandra', 'Paulina', 'Jennifer', 'Shakira', 'Marie', 'Sabrina', 'Steffi', 'Kim', 'Darya'], 4), (['Alicia', 'Jennifer', 'Kim', 'Marie', 'Paulina', 'Sabrina', 'Sandra', 'Shakira', 'Steffi', 'Darya'], 3)]
truthBooth_denied = [('Danilo', 'Jennifer'), ('Elia', 'Jennifer'), ('Mike', 'Kim'), ('Teezy', 'Alicia')]
truthBooth_confirmed = [('Danilo', 'Darya')]

# Helper Functions
def correlation(list1, list2):
    total = 0
    for i in range(len(list1)):
        if list1[i] == list2[i]:
            total += 1
    return total

def isImpossible(matchlist):
    for match in truthBooth_denied:
        if tuple(sorted([match[0], match[1]])) in matchlist:
            return True
    for match in truthBooth_confirmed:
        if tuple(sorted([match[0], match[1]])) not in matchlist:
            return True
    for week in allWeeks:
        if correlation(matchlist, week[0]) != week[1]:
            return True        
    return False

# Main Program
possible = []
if load_from_file:
    iterable = pickle.load(open("allmatches.p", "rb"))
else:
    iterable = itertools.combinations([(m, w) for m in men for w in women], len(men))

for matching in iterable:
    if isImpossible(matching):
        continue
    else:
        possible.append(matching)

# Additional code and statistics can be added here

# Save possible matches to file
pickle.dump(possible, open("allmatches.p", "wb"))
