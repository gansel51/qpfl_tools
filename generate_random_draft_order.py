"""
QPFL Offensive Line Draft 2024
"""

import random

teams = [
    "Griffin",
    "Ryan",
    "Kaminska",
    "Reardon",
    "Stephen",
    "Spencer/Tim",
    "Joe/Joe",
    "Anagh",
    "Bill",
    "Arnav",
]

first_round = random.sample(teams, len(teams))
second_round = first_round[::-1]
combined_order = first_round + second_round

for team in combined_order:
    print(team)
