# Trigger warning: Sexism
# To make the code correctly identify possible couples, man's name
# needs to be written first, followed by the woman's name.

from tqdm import tqdm  # progress bar only
import itertools
import pandas as pd
import math

# ===== AYTO VIP 2025 (current through MN4) =====
# Cast (normalized spellings). 11 men, 11 women incl. 'SIT' as dummy.
men = [
    'Calvin O.', 'Calvin S.', 'Kevin', 'Leandro', 'Lennert',
    'Nico', 'Olli', 'Rob', 'Sidar', 'Xander', 'Jonny'
]
women = [
    'Antonia', 'Ariel', 'Beverly', 'Elli', 'Hati',
    'Henna', 'Joanna', 'Nelly', 'Sandra', 'Viki', 'SIT'  # 'SIT' is the sitter slot
]

# Weekly seatings (Matching Nights) and beam counts.
# IMPORTANT: We exclude the ('<man>','SIT') pair from each night list,
# because beams count ONLY real couples, not the sitter.
allWeeks = [
    # MN1 — beams = 2
    ([
        ('Leandro','Viki'),
        ('Calvin O.','Hati'),
        ('Jonny','Henna'),
        ('Sidar','Nelly'),
        ('Kevin','Sandra'),
        ('Rob','Joanna'),
        ('Nico','Ariel'),
        ('Lennert','Antonia'),
        ('Xander','Elli'),
        ('Calvin S.','Beverly'),
    ], 2),
    # MN2 — beams = 2
    ([
        ('Calvin S.','Joanna'),
        ('Rob','Nelly'),
        ('Kevin','Sandra'),
        ('Nico','Ariel'),
        ('Sidar','Beverly'),
        ('Olli','Henna'),
        ('Calvin O.','Hati'),
        ('Leandro','Viki'),
        ('Jonny','Antonia'),
        ('Xander','Elli'),
    ], 2),
    # MN3 — beams = 2
    ([
        ('Calvin S.','Joanna'),
        ('Olli','Antonia'),
        ('Nico','Beverly'),
        ('Calvin O.','Ariel'),
        ('Rob','Hati'),
        ('Leandro','Henna'),
        ('Kevin','Sandra'),
        ('Jonny','Viki'),
        ('Lennert','Nelly'),
        ('Xander','Elli'),  # sat separately this night but still a seat in some reports; keep consistent
    ], 2),
    # MN4 — beams = 3
    ([
        ('Calvin S.','Joanna'),
        ('Calvin O.','Nelly'),
        ('Leandro','Sandra'),
        ('Nico','Ariel'),
        ('Sidar','Beverly'),
        ('Lennert','Henna'),
        ('Kevin','Viki'),
        ('Rob','Hati'),
        ('Olli','Antonia'),
        ('Xander','Elli'),
    ], 3),
]

# Truth Booth (Matchbox) results that are confirmed NOT a match (NM).
# Only include NM here; PMs (like Xander–Elli) are implicitly allowed by the weeks.
truthBooth_denied = [
    ('Jonny','Beverly'),    # NM
    ('Leandro','Sandra'),   # NM
    ('Calvin S.','Nelly'),  # NM
    # add more NM pairs as they air, always (man, woman)
]

# --------- helpers ----------
def correlation(list1, list2):
    """Count overlapping couples between two lists, ignoring any SIT pairs."""
    s2 = set(list2)
    total = 0
    for (m, w) in list1:
        if w == 'SIT':
            continue
        if (m, w) in s2:
            total += 1
    return total

def isImpossible(matchlist):
    # Disallow any Truth Booth NM pairs
    for match in truthBooth_denied:
        if match in matchlist:
            return True
    # Enforce each Matching Night's beam count
    for seats, beams in allWeeks:
        if correlation(matchlist, seats) != beams:
            return True
    return False

# --------- exhaustive enumeration with a single progress bar ----------
possible = []

# We allow exactly one man to be matched to 'SIT' in any full assignment.
# Since women includes 'SIT' and len(men) == len(women) == 11, permutations
# will naturally assign one man to 'SIT'.
iterable = itertools.permutations(women, len(men))
total_iterations = math.factorial(len(women))  # 11! permutations

for matching in tqdm(iterable, total=total_iterations, unit='assign', desc='Enumerating'):
    matchlist = list(zip(men, matching))
    if isImpossible(matchlist):
        continue
    possible.append(matchlist)

# Flatten all feasible full matchings into a pair table
flattened_possible = [match for sublist in possible for match in sublist]
df = pd.DataFrame(flattened_possible, columns=['Man', 'Woman'])

print(df)
