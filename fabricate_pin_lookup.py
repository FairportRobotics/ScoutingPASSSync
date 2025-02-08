import random

team_members = [
    "Abyss Mortimer",
    "Alex Phillips",
    "Amanah Obaji",
    "Andrew McCadden",
    "Ariana Toner",
    "Asher Stuckey",
    "Autumn Schoenfeld",
    "Brandon Bates",
    "Carter Silva",
    "Celton Norter",
    "Colby Jackson",
    "Colden Stubbe",
    "Connor Toper",
    "Dean Blanchard",
    "Domenic Giammusso",
    "Greydon Jones-Dulisse",
    "Hamza Keles",
    "Jackson Newcomb",
    "Jacob LeBlanc",
    "Jacob Wyrozebski",
    "Jesse White",
    "Jonah Woika",
    "Jonathan Brouillard",
    "Jordan Fenton",
    "Kai Hurrell",
    "Kai Wilbur",
    "Lukas Harrison",
    "Maddie DeCicca",
    "Mason Silva",
    "Matthew Mazzota",
    "Nanson Chen",
    "Nicholas Munier",
    "Ruthie Christensen",
    "Sam Clark",
    "Shawn Estrich",
    "Siena Reeve",
    "Simon Stuckey",
    "TJ Blake",
    "Tyler Hignett",
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

