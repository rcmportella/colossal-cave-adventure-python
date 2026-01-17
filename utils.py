"""
Utility functions for Colossal Cave Adventure
"""
import random
import sys


def speak(message_id, messages):
    """Print a game message by ID"""
    if message_id in messages:
        msg = messages[message_id]
        if isinstance(msg, list):
            for line in msg:
                print(line)
        else:
            print(msg)
        print()


def get_input(prompt=""):
    """Get input from user and parse it into words"""
    if prompt:
        print(prompt)
    
    try:
        line = input("> ").strip().upper()
    except EOFError:
        print("\nGoodbye!")
        sys.exit(0)
    
    if not line:
        return None, None
    
    # Split input into words
    words = line.split()
    
    if len(words) == 0:
        return None, None
    elif len(words) == 1:
        return words[0], None
    else:
        return words[0], words[1]


def yes_no_question(question_msg, yes_msg, no_msg, messages):
    """Ask a yes/no question and return True for yes, False for no"""
    speak(question_msg, messages)
    
    while True:
        response, _ = get_input()
        if response in ['YES', 'Y']:
            if yes_msg:
                speak(yes_msg, messages)
            return True
        elif response in ['NO', 'N']:
            if no_msg:
                speak(no_msg, messages)
            return False
        else:
            print("Please answer YES or NO.")


def random_chance(probability):
    """Return True with given probability (0.0 to 1.0)"""
    return random.random() < probability


def describe_location(location, long_desc, short_desc, abbrev_count, is_dark):
    """Print location description"""
    if is_dark:
        return
    
    # Use long description if first time or abbrev_count is 0
    if abbrev_count == 0 and location in long_desc:
        for line in long_desc[location]:
            print(line)
        print()
    elif location in short_desc:
        print(short_desc[location])
        print()
    elif location in long_desc:
        # Fallback to long description if short description doesn't exist
        for line in long_desc[location]:
            print(line)
        print()


def list_available_movements(location, travel_table, vocabulary, object_place=None):
    """List all available commands at the current location"""
    print("Available commands at this location:")
    print()
    
    # Magic words that should not be revealed (player must discover them)
    magic_codes = {48, 65, 55}  # XYZZY, PLUGH, Y2
    
    # 1. Movement commands
    if location in travel_table:
        available_motions = travel_table[location].keys()
        
        # Find words that map to these motion codes
        movement_words = {}
        for word, value in vocabulary.items():
            # Only consider motion words (not tuples)
            if not isinstance(value, tuple):
                if value in available_motions and value not in magic_codes:
                    if value not in movement_words:
                        movement_words[value] = []
                    movement_words[value].append(word)
        
        if movement_words:
            print("Movement:")
            # Sort by motion code for consistent ordering
            for motion_code in sorted(movement_words.keys()):
                words = movement_words[motion_code]
                # Show the shortest/most common word for each direction
                primary_word = min(words, key=len)
                print(f"  {primary_word.upper()}")
            print()
    
    # 2. Objects at this location
    if object_place:
        objects_here = []
        for word, value in vocabulary.items():
            if isinstance(value, tuple) and value[1] == 1:  # Object type
                obj_id = value[0]
                if obj_id in object_place and object_place[obj_id] == location:
                    objects_here.append(word)
        
        if objects_here:
            print("Objects you can interact with:")
            # Remove duplicates and sort
            unique_objects = sorted(set(objects_here))
            for obj in unique_objects:
                print(f"  {obj.upper()}")
            print()
    
    # 3. General commands always available
    print("General commands:")
    print("  INVENTORY (I) - check what you're carrying")
    print("  LOOK (L) - look around again")
    print("  QUIT - quit the game")
    print()


def describe_objects(location, objects, object_place, object_props, object_desc):
    """Describe visible objects at location"""
    # Find all objects at this location
    visible_objects = []
    for obj_id, obj_loc in object_place.items():
        if obj_loc == location and obj_id in object_desc:
            visible_objects.append(obj_id)
    
    for obj_id in visible_objects:
        # Modify description based on object state/properties
        desc = object_desc[obj_id]
        prop = object_props.get(obj_id, 0)
        
        # Special cases for certain objects
        if obj_id == 3 and prop == 0:  # Grate locked
            desc = "The grate is locked."
        elif obj_id == 3 and prop == 1:  # Grate unlocked
            desc = "The grate is unlocked."
        
        print(desc)
    
    if visible_objects:
        print()


def list_inventory(object_place):
    """List objects being carried"""
    carried = []
    for obj_id, obj_loc in object_place.items():
        if obj_loc == -1:  # -1 means being carried
            carried.append(obj_id)
    
    if not carried:
        print("You are empty-handed.")
    else:
        print("You are currently holding:")
        for obj_id in carried:
            obj_name = get_object_name(obj_id)
            print(f"  {obj_name}")
    print()


def get_object_name(obj_id):
    """Get printable name for object"""
    names = {
        1: "Keys",
        2: "Lamp",
        3: "Grate",
        4: "Cage",
        5: "Rod",
        7: "Bird",
        10: "Gold nugget",
        11: "Snake",
        19: "Food",
        20: "Water bottle",
        21: "Axe",
    }
    return names.get(obj_id, f"Object {obj_id}")


def parse_command(word1, word2, vocabulary):
    """Parse command words using vocabulary"""
    if not word1:
        return None, None, None
    
    # Check first word
    if word1 not in vocabulary:
        return None, None, None
    
    word1_data = vocabulary[word1]
    
    # Motion verb (simple integer)
    if isinstance(word1_data, int):
        return 0, word1_data, word2
    
    # Object or action verb (tuple)
    if isinstance(word1_data, tuple):
        code, word_type = word1_data
        return word_type, code, word2
    
    return None, None, word2


def can_see(location, lamp_location, lamp_on, location_conditions):
    """Check if player can see in current location"""
    # If location has light naturally (condition & 1 == 0)
    if location in location_conditions:
        if location_conditions[location] % 2 == 0:
            return True
    
    # Or if carrying lit lamp
    if lamp_location == -1 and lamp_on:
        return True
    
    # Or if lamp is at current location and lit
    if lamp_location == location and lamp_on:
        return True
    
    return False
