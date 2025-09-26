import random

team_members = [
    "Dean Blanchard ",
    "Rachel Case ",
    "Ruth Christensen ",
    "Andrew Crawford  ",
    "Gianmarco D'Angelo  ",
    "Vaishu Das ",
    "Madison DeCicca ",
    "Nathan DeVito ",
    "Domenic Giammusso ",
    "Eli Harrison ",
    "Tyler Hignett ",
    "Runa Hunt ",
    "Colby Jackson ",
    "Matthew Mazzota ",
    "Caitlin Munier ",
    "Nicholas Munier ",
    "Celton Norter ",
    "Amanah Obaji ",
    "Connor Rapp ",
    "Arthur Sayre ",
    "Autumn Schoenfeld ",
    "Mason Silva ",
    "Carter Silva ",
    "Ethan Stiffler ",
    "Tetra Ukav ",
    "Kai  Wilbur ",
    "Jonah Woika ",
    "Unknown ",
]


# Generate a list of numbers from 1000 to 9999
numbers = list(range(1000, 10000))

# Enumerate the members and pick a random number.
for member in team_members:
    # Pick a random number
    random_number = random.choice(numbers)

    # Remove the selected number
    numbers.remove(random_number)    
    print(f"'{random_number}': '{member}',")

