"""
Game data for Colossal Cave Adventure
Contains locations, objects, text messages, and game state data
"""

# Object constants
KEYS = 1
LAMP = 2
GRATE = 3
CAGE = 4
ROD = 5
BIRD = 7
NUGGET = 10
SNAKE = 11
FOOD = 19
WATER = 20
AXE = 21

# Initial object placements (location where object starts)
initial_placements = {
    1: 3, 2: 3, 3: 8, 4: 10, 5: 11, 6: 14, 7: 13, 8: 9,
    9: 15, 10: 18, 11: 19, 12: 17, 13: 27, 14: 28, 15: 29,
    16: 30, 17: 0, 18: 0, 19: 3, 20: 3
}

# Fixed objects (cannot be picked up)
fixed_objects = {
    3: True, 6: True, 8: True, 9: True, 12: True, 13: True
}

# Dwarf travel table
dwarf_travel = [
    36, 28, 19, 30, 62, 60, 41, 27, 17, 15, 19, 28, 36, 300, 300
]

# Question/response indices
quip_responses = [50, 51, 64, 66, 67, 68, 69, 49, 79]

# Verb-specific messages
verb_messages = [24, 29, 0, 31, 0, 31, 38, 38, 42, 42, 43, 46, 77, 71, 73, 75]

# Location conditions (1 = requires light, 2 = no question, 0 = has natural light)
location_conditions = {}
# Locations 1-10 have natural light (outside)
for i in range(1, 11):
    location_conditions[i] = 0  # Changed to 0 for natural light

# Dark locations that need lamp
location_conditions.update({
    16: 2, 20: 2, 21: 2, 22: 2, 23: 2, 24: 2,
    25: 2, 26: 2, 31: 2, 32: 2, 79: 2
})

# Game messages (these would normally be loaded from external file)
messages = {
    2: "There are threatening little dwarves in the room with you!",
    3: "There is a threatening little dwarf in the room with you!",
    4: "The dwarf throws a knife at you.",
    5: "The dwarf throws a knife at you but misses!",
    6: "One of them gets you!",
    7: "The dwarf's knife misses you!",
    8: "A hollow voice says 'PLUGH'.",
    9: "I don't understand that!",
    10: "I don't know how to apply that word here.",
    11: "I don't know that word.",
    12: "I don't understand that!",
    13: "I don't understand that!",
    14: "(Long descriptions are suppressed. Use LOOK to see full descriptions.)",
    15: "You are already carrying it!",
    16: "It is now pitch dark. If you proceed you will likely fall into a pit.",
    17: "If you prefer, simply type W rather than WEST.",
    18: "Are you trying to catch the bird?",
    19: "The bird is caught.",
    20: "Are you trying to somehow deal with the snake?",
    21: "You can't kill the snake, or drive it away, or avoid it, or anything like that. There is a way to get by, but you don't have the necessary resources right now.",
    22: "The rod is too heavy. You'll have to leave something behind.",
    23: "A hollow voice says 'PLOVER'.",
    24: "Game over.",
    25: "The bird's cage is still locked.",
    26: "You can catch the bird, but you cannot carry it.",
    27: "The bird seems frightened. Perhaps if you got rid of the rod...",
    28: "There is nothing here to which the chain can be locked.",
    30: "The little bird attacks the green snake, and in an astounding flurry gets killed.",
    32: "The grate is locked.",
    33: "You have no keys!",
    34: "The grate is now unlocked.",
    35: "The grate is now locked.",
    36: "It was already locked.",
    37: "The grate is now unlocked.",
    39: "Your lamp is now on.",
    40: "Your lamp is now off.",
    42: "The stream is flowing into a low passage and you can't get through.",
    44: "Attacking the dwarf is bad idea.",
    45: "The little bird is now dead. Its body disappears.",
    47: "The dwarf runs away.",
    48: "You killed a little dwarf.",
    49: "Enter the stream?",
    50: "The grate is locked and you don't have the keys.",
    52: "You scored a direct hit!",
    54: "OK",
    55: "You can't unlock the keys.",
    56: "The mist is very thick here.",
    57: "You have crawled around in some little holes and wound up back in the main passage.",
    58: "You have crawled around in some little holes and found your way blocked by a recent cave-in.",
    59: "Go where?",
    60: "I don't understand that!",
    61: "What?",
    62: "Are you trying to get into the cave?",
    63: "The grate is very solid and has a hardened steel lock. You cannot enter without a key, and there are no keys in sight.",
    64: "I respectfully suggest you go across the bridge instead of jumping.",
    65: "Welcome to Adventure! Would you like instructions?",
    66: "Digging without a shovel is quite impractical. Even with a shovel progress is unlikely.",
    67: "Blasting requires dynamite.",
    68: "I'm game. Would you care to explain how?",
    69: "Sorry, but I am not allowed to give more detail. I will repeat the long description of your location.",
    71: "It is now pitch black. Your lamp has run out of power.",
    72: "Thank you, it was delicious!",
    74: "The bottle of water is now empty.",
    76: "Rubbing the lamp is not particularly rewarding. Anyway, nothing exciting happens.",
    77: "Where?",
    78: "Your bottle is empty and the ground is wet.",
    79: "You have taken a rare photograph.",
    80: "I beg your pardon?",
    100: "Do you really want to quit now?"
}

# Location descriptions (short form)
short_descriptions = {
    1: "You're at end of road again.",
    2: "You're at hill in road.",
    3: "You're inside building.",
    4: "You're in valley.",
    5: "You're in forest.",
    6: "You're in forest.",
    7: "You're at slit in streambed.",
    8: "You're outside grate.",
    9: "You're below the grate.",
    10: "You're in cobble crawl.",
    13: "You're in bird chamber.",
    14: "You're at top of small pit.",
    15: "You're in hall of mists.",
    19: "You're in a low room.",
    20: "You're on east bank of fissure.",
    27: "You're at west end of twopit room.",
    31: "You're at a splendid chamber.",
    32: "You're at junction of three secret canyons.",
    33: "You're in large low room.",
    65: "You're in misty cavern.",
    68: "You're in oriental room.",
    71: "You're in secret canyon.",
}

# Long location descriptions
long_descriptions = {
    1: ["You are standing at the end of a road before a small brick building.",
        "Around you is a forest. A small stream flows out of the building and",
        "down a gully."],
    2: ["You have walked up a hill, still in the forest. The road slopes back",
        "down the other side of the hill. There is a building in the distance."],
    3: ["You are inside a building, a well house for a large spring.",
        "There are some keys on the ground here.",
        "There is a shiny brass lamp nearby.",
        "There is food here.",
        "There is a bottle of water here."],
    4: ["You are in a valley in the forest beside a stream tumbling along a",
        "rocky bed."],
    5: ["You are in open forest, with a deep valley to one side."],
    6: ["You are in open forest near both a valley and a road."],
    7: ["At your feet all the water of the stream splashes into a 2-inch slit",
        "in the rock. Downstream the streambed is bare rock."],
    8: ["You are in a 20-foot depression floored with bare dirt. Set into the",
        "dirt is a strong steel grate mounted in concrete. A dry streambed",
        "leads into the depression."],
    9: ["You are in a small chamber beneath a 3x3 steel grate to the surface.",
        "A low crawl over cobbles leads inward to the west."],
}

# Object descriptions
object_descriptions = {
    KEYS: "There are some keys on the ground here.",
    LAMP: "There is a shiny brass lamp nearby.",
    GRATE: "The grate is locked.",
    BIRD: "A cheerful little bird is sitting here singing.",
    NUGGET: "There is a large sparkling nugget of gold here!",
    SNAKE: "A huge green fierce snake bars the way!",
    FOOD: "There is food here.",
    WATER: "There is a bottle of water here.",
    AXE: "There is a little axe here.",
}

# Vocabulary - words and their numeric codes
vocabulary = {
    # Motion verbs (type 0)
    'NORTH': 1, 'N': 1,
    'SOUTH': 2, 'S': 2,
    'EAST': 3, 'E': 3,
    'WEST': 4, 'W': 4,
    'UP': 5, 'U': 5,
    'DOWN': 6, 'D': 6,
    'IN': 7, 'INSI': 7, 'INSID': 7, 'INSIDE': 7,
    'OUT': 8, 'OUTSI': 8, 'OUTSIDE': 8,
    'QUIT': 17,
    'ENTER': 29,
    'STREAM': 30,
    
    # Objects (type 1)
    'KEYS': (KEYS, 1), 'KEY': (KEYS, 1),
    'LAMP': (LAMP, 1), 'LANTERN': (LAMP, 1), 'HEADLAMP': (LAMP, 1),
    'GRATE': (GRATE, 1),
    'CAGE': (CAGE, 1),
    'ROD': (ROD, 1),
    'BIRD': (BIRD, 1),
    'GOLD': (NUGGET, 1), 'NUGGET': (NUGGET, 1),
    'SNAKE': (SNAKE, 1),
    'FOOD': (FOOD, 1), 'RATION': (FOOD, 1),
    'WATER': (WATER, 1), 'BOTTLE': (WATER, 1),
    'AXE': (AXE, 1),
    
    # Action verbs (type 2)
    'TAKE': (1, 2), 'CARRY': (1, 2), 'KEEP': (1, 2), 'CATCH': (1, 2),
    'DROP': (2, 2), 'RELEASE': (2, 2), 'FREE': (2, 2), 'DISCARD': (2, 2),
    'INVENTORY': (3, 2), 'INVEN': (3, 2), 'I': (3, 2),
    'LOCK': (4, 2),
    'UNLOCK': (6, 2),
    'LIGHT': (7, 2), 'ON': (7, 2),
    'EXTINGUISH': (8, 2), 'OFF': (8, 2),
    'STRIKE': (9, 2), 'IGNITE': (9, 2),
    'LOOK': (10, 2), 'L': (10, 2), 'EXAMINE': (10, 2),
    'ATTACK': (12, 2), 'KILL': (12, 2), 'FIGHT': (12, 2),
    'EAT': (13, 2),
    'DRINK': (14, 2),
    'RUB': (15, 2),
    'POUR': (16, 2),
}

# Travel table - format: {location: {motion_code: new_location}}
# Simplified travel table for key locations
travel_table = {
    1: {4: 2, 7: 3, 5: 4, 1: 2, 2: 5},  # End of road
    2: {1: 1, 4: 1, 2: 5, 3: 5},  # Hill in road
    3: {8: 1, 11: 1},  # Inside building
    4: {1: 2, 3: 6, 4: 7, 5: 5, 2: 8},  # Valley
    5: {1: 2, 3: 6, 4: 5, 2: 5},  # Forest
    6: {2: 1, 4: 5, 1: 5},  # Forest
    7: {1: 4, 2: 8, 5: 6},  # Slit in streambed
    8: {4: 7, 7: 3, 6: 9},  # Outside grate (if unlocked)
    9: {5: 8, 4: 10},  # Below grate
    10: {4: 9, 3: 11},  # Cobble crawl
}
