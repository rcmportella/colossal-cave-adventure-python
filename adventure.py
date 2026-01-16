#!/usr/bin/env python3
"""
Colossal Cave Adventure
Python translation of the original 1976 Fortran game

This is a text adventure game where you explore a cave system,
collect treasures, and avoid dangers.
"""

import random
import sys
from game_data import *
from utils import *


class Adventure:
    def __init__(self):
        """Initialize game state"""
        # Object locations (-1 = carried, 0 = nowhere, positive = location)
        self.object_place = initial_placements.copy()
        
        # Object properties/states
        self.object_props = {}
        for obj in self.object_place.keys():
            self.object_props[obj] = 0
        
        # Fixed objects (cannot be picked up)
        self.fixed = fixed_objects.copy()
        
        # Location visit counts for abbreviation
        self.location_abbrev = {}
        for i in range(300):
            self.location_abbrev[i] = 0
        
        # Player state
        self.location = 1  # Start at end of road
        self.old_location = 1
        
        # Lamp state
        self.lamp_on = False
        
        # Dwarf state
        self.dwarf_stage = 0  # 0=not started, 1=waiting, 2+=active
        self.dwarf_locations = [0, 0, 0]
        self.old_dwarf_locations = [0, 0, 0]
        self.dwarf_seen = [False, False, False]
        
        # Game flags
        self.first_time = True
        self.west_count = 0
        self.detail_count = 0
        
        # Grate state
        self.grate_locked = True
    
    def run(self):
        """Main game loop"""
        # Initial instructions
        if yes_no_question(65, 0, 0, messages):
            self.show_instructions()
        
        # Main game loop
        while True:
            self.turn()
    
    def show_instructions(self):
        """Show game instructions"""
        print("""
Somewhere nearby is Colossal Cave, where others have found fortunes in
treasure and gold, though it is rumored that some who enter are never
seen again. Magic is said to work in the cave. I will be your eyes
and hands. Direct me with commands of one or two words.

(Should you get stuck, type "QUIT" to exit.)

This program was originally developed by Willie Crowther. Most of the
features of the current program were added by Don Woods.
        """)
    
    def turn(self):
        """Execute one game turn"""
        # Check for dwarves
        self.check_dwarves()
        
        # Describe location
        is_dark = not can_see(self.location, self.object_place.get(LAMP),
                             self.lamp_on, location_conditions)
        
        if is_dark:
            speak(16, messages)
        else:
            # Show location description
            describe_location(self.location, long_descriptions, short_descriptions,
                            self.location_abbrev.get(self.location, 0), False)
            # Show objects at location
            describe_objects(self.location, None, self.object_place,
                           self.object_props, object_descriptions)
        
        # Update abbreviation counter
        if self.location in self.location_abbrev:
            self.location_abbrev[self.location] = (self.location_abbrev[self.location] + 1) % 5
        else:
            self.location_abbrev[self.location] = 1
        
        # Get command
        trouble_count = 0
        while True:
            word1, word2 = get_input()
            
            if word1 is None:
                continue
            
            # Special handling for "ENTER STREAM/WATER"
            if word1 == "ENTER" and word2 in ["STREAM", "WATER"]:
                speak(70, messages)
                continue
            
            # Parse command
            word_type, code, remaining = parse_command(word1, word2, vocabulary)
            
            if word_type is None:
                # Unknown word
                trouble_count += 1
                if trouble_count >= 3:
                    if not self.offer_help():
                        trouble_count = 0
                msg_id = random.choice([60, 61, 13])
                speak(msg_id, messages)
                continue
            
            # Process command based on type
            if word_type == 0:  # Motion
                if self.do_motion(code):
                    break
            elif word_type == 1:  # Object
                # Need a verb
                if word2:
                    word_type2, code2, _ = parse_command(word2, None, vocabulary)
                    if word_type2 == 2:  # Action verb
                        if self.do_action(code2, code):
                            break
                    else:
                        print(f"What do you want to do with the {word1}?")
                else:
                    print(f"What do you want to do with the {word1}?")
            elif word_type == 2:  # Action verb
                if code == 3:  # Inventory
                    list_inventory(self.object_place)
                elif code == 10:  # Look
                    self.location_abbrev[self.location] = 0
                    break
                else:
                    # Need an object
                    if word2:
                        word_type2, code2, _ = parse_command(word2, None, vocabulary)
                        if word_type2 == 1:  # Object
                            if self.do_action(code, code2):
                                break
                        else:
                            print(f"{word1} what?")
                    else:
                        # Try to infer object
                        if self.infer_object(code):
                            break
                        else:
                            print(f"{word1} what?")
    
    def do_motion(self, motion_code):
        """Handle movement commands"""
        # Special motion codes
        if motion_code == 17:  # QUIT
            if yes_no_question(22, 0, 0, {"22": "Do you really want to quit now?"}):
                print("OK. Goodbye!")
                sys.exit(0)
            return False
        
        # Track west commands
        if motion_code == 4:  # WEST
            self.west_count += 1
            if self.west_count == 10:
                speak(17, messages)
        
        # Check travel table
        if self.location in travel_table and motion_code in travel_table[self.location]:
            new_loc = travel_table[self.location][motion_code]
            
            # Check for special location codes (>= 300)
            if new_loc >= 300:
                new_loc = self.handle_special_location(new_loc)
            
            self.old_location = self.location
            self.location = new_loc
            return True
        else:
            # Can't go that way
            speak(12, messages)
            return False
    
    def handle_special_location(self, special_code):
        """Handle special location transitions"""
        offset = special_code - 300
        
        if offset == 1:  # Random choice between two locations
            return 5 if random_chance(0.5) else 6
        elif offset == 2:  # Grate check (going down)
            return 9 if self.object_props.get(GRATE, 0) == 1 else 23
        elif offset == 3:  # Grate check (going up)
            return 8 if self.object_props.get(GRATE, 0) == 1 else 9
        else:
            return self.location
    
    def do_action(self, verb_code, obj_code):
        """Handle action verbs"""
        obj_location = self.object_place.get(obj_code, 0)
        
        # Check if object is present
        if obj_location != self.location and obj_location != -1:
            print(f"I don't see that here.")
            return False
        
        # TAKE/CARRY
        if verb_code == 1:
            return self.do_take(obj_code)
        
        # DROP
        elif verb_code == 2:
            return self.do_drop(obj_code)
        
        # LOCK
        elif verb_code == 4:
            return self.do_lock(obj_code)
        
        # UNLOCK
        elif verb_code == 6:
            return self.do_unlock(obj_code)
        
        # LIGHT/ON
        elif verb_code == 7:
            return self.do_light(obj_code)
        
        # EXTINGUISH/OFF
        elif verb_code == 8:
            return self.do_extinguish(obj_code)
        
        # STRIKE
        elif verb_code == 9:
            if obj_code == 12:  # Matches
                self.object_props[12] = 1
                print("The match flares up.")
                return True
            else:
                speak(54, messages)
                return False
        
        # ATTACK
        elif verb_code == 12:
            return self.do_attack(obj_code)
        
        # EAT
        elif verb_code == 13:
            return self.do_eat(obj_code)
        
        # DRINK
        elif verb_code == 14:
            return self.do_drink(obj_code)
        
        # RUB
        elif verb_code == 15:
            if obj_code == LAMP:
                speak(76, messages)
            else:
                speak(54, messages)
            return False
        
        # POUR
        elif verb_code == 16:
            return self.do_pour(obj_code)
        
        speak(54, messages)
        return False
    
    def do_take(self, obj_code):
        """Take/carry an object"""
        if obj_code == 18:  # Water (special case)
            speak(54, messages)
            return False
        
        obj_location = self.object_place.get(obj_code, 0)
        
        if obj_location == -1:
            print("You are already carrying it!")
            return False
        
        if obj_location != self.location:
            print("I don't see that here.")
            return False
        
        if self.fixed.get(obj_code, False):
            speak(25, messages)
            return False
        
        # Special cases
        if obj_code == BIRD and self.object_place.get(ROD, 0) == -1:
            speak(26, messages)
            return False
        
        # Take the object
        self.object_place[obj_code] = -1
        speak(54, messages)
        return True
    
    def do_drop(self, obj_code):
        """Drop an object"""
        if obj_code == 18:  # Water (special case)
            speak(54, messages)
            return False
        
        if self.object_place.get(obj_code, 0) != -1:
            print("You aren't carrying it!")
            return False
        
        # Special case: bird and snake
        if obj_code == BIRD and self.location == 19 and self.object_props.get(SNAKE, 0) == 0:
            speak(30, messages)
            self.object_props[SNAKE] = 1
        
        self.object_place[obj_code] = self.location
        speak(54, messages)
        return True
    
    def do_lock(self, obj_code):
        """Lock something"""
        if obj_code == GRATE:
            if self.object_place.get(KEYS, 0) not in [self.location, -1]:
                speak(33, messages)
                return False
            
            if self.object_props.get(GRATE, 0) == 1:
                speak(35, messages)
                self.object_props[GRATE] = 0
                return True
            else:
                speak(36, messages)
                return False
        else:
            speak(28, messages)
            return False
    
    def do_unlock(self, obj_code):
        """Unlock something"""
        if obj_code == GRATE:
            if self.object_place.get(KEYS, 0) not in [self.location, -1]:
                speak(33, messages)
                return False
            
            if self.object_props.get(GRATE, 0) == 0:
                speak(37, messages)
                self.object_props[GRATE] = 1
                return True
            else:
                speak(36, messages)
                return False
        else:
            speak(28, messages)
            return False
    
    def do_light(self, obj_code):
        """Light the lamp"""
        if obj_code != LAMP:
            print("You can't light that!")
            return False
        
        if self.object_place.get(LAMP, 0) not in [self.location, -1]:
            print("I don't see a lamp here.")
            return False
        
        self.lamp_on = True
        speak(39, messages)
        return True
    
    def do_extinguish(self, obj_code):
        """Extinguish the lamp"""
        if obj_code != LAMP:
            print("You can't extinguish that!")
            return False
        
        if self.object_place.get(LAMP, 0) not in [self.location, -1]:
            print("I don't see a lamp here.")
            return False
        
        self.lamp_on = False
        speak(40, messages)
        return True
    
    def do_attack(self, obj_code):
        """Attack something"""
        # Check for dwarves first
        for i in range(3):
            if self.dwarf_seen[i]:
                if random_chance(0.4):
                    self.dwarf_seen[i] = False
                    self.dwarf_locations[i] = 0
                    self.old_dwarf_locations[i] = 0
                    speak(47, messages)
                else:
                    speak(48, messages)
                return True
        
        if obj_code == SNAKE:
            print("Attacking the snake is pointless.")
            return False
        elif obj_code == BIRD:
            speak(45, messages)
            self.object_place[BIRD] = 0
            return True
        else:
            speak(44, messages)
            return False
    
    def do_eat(self, obj_code):
        """Eat something"""
        if obj_code == FOOD:
            if self.object_place.get(FOOD, 0) in [self.location, -1]:
                if self.object_props.get(FOOD, 0) == 0:
                    self.object_props[FOOD] = 1
                    speak(72, messages)
                    return True
        speak(54, messages)
        return False
    
    def do_drink(self, obj_code):
        """Drink something"""
        if obj_code == WATER:
            if self.object_place.get(WATER, 0) in [self.location, -1]:
                if self.object_props.get(WATER, 0) == 0:
                    self.object_props[WATER] = 1
                    speak(74, messages)
                    return True
        speak(54, messages)
        return False
    
    def do_pour(self, obj_code):
        """Pour something"""
        if obj_code == WATER:
            self.object_props[WATER] = 1
            speak(78, messages)
            return True
        speak(54, messages)
        return False
    
    def infer_object(self, verb_code):
        """Try to infer object from context"""
        # For single-object rooms, infer the object
        objects_here = []
        for obj_id, obj_loc in self.object_place.items():
            if obj_loc == self.location or obj_loc == -1:
                objects_here.append(obj_id)
        
        if len(objects_here) == 1 and verb_code not in [3, 10]:  # Not inventory or look
            return self.do_action(verb_code, objects_here[0])
        
        return False
    
    def offer_help(self):
        """Offer contextual help"""
        # At grate
        if self.location == 8 and self.object_props.get(GRATE, 0) == 0:
            if yes_no_question(62, 63, 54, messages):
                return True
        
        # With bird and pit
        if self.location == 13 and self.object_place.get(BIRD, 0) == 13 and \
           self.object_place.get(ROD, 0) != -1:
            if yes_no_question(18, 19, 54, messages):
                return True
        
        # With snake
        if self.location == 19 and self.object_props.get(SNAKE, 0) == 0 and \
           self.object_place.get(BIRD, 0) == -1:
            if yes_no_question(20, 21, 54, messages):
                return True
        
        return False
    
    def check_dwarves(self):
        """Handle dwarf encounters"""
        # Start dwarves at location 15
        if self.dwarf_stage == 0:
            if self.location == 15:
                self.dwarf_stage = 1
            return
        
        # Initial delay
        if self.dwarf_stage == 1:
            if random_chance(0.05):
                self.dwarf_stage = 2
                for i in range(3):
                    self.dwarf_locations[i] = 0
                    self.old_dwarf_locations[i] = 0
                    self.dwarf_seen[i] = False
                speak(3, messages)
                # Place axe
                self.object_place[AXE] = self.location
            return
        
        # Move dwarves
        self.dwarf_stage += 1
        attack_count = 0
        dwarves_present = 0
        hit_count = 0
        
        for i in range(3):
            if 2 * i + self.dwarf_stage < 8:
                continue
            if 2 * i + self.dwarf_stage > 23 and not self.dwarf_seen[i]:
                continue
            
            self.old_dwarf_locations[i] = self.dwarf_locations[i]
            
            if not self.dwarf_seen[i] and self.location > 14:
                # Move dwarf
                idx = i * 2 + self.dwarf_stage - 8
                if idx < len(dwarf_travel):
                    self.dwarf_locations[i] = dwarf_travel[idx]
            
            if self.dwarf_locations[i] == self.location or \
               self.old_dwarf_locations[i] == self.location:
                self.dwarf_seen[i] = True
                self.dwarf_locations[i] = self.location
                dwarves_present += 1
                
                if self.old_dwarf_locations[i] == self.dwarf_locations[i]:
                    attack_count += 1
                    if random_chance(0.1):
                        hit_count += 1
        
        if dwarves_present == 0:
            return
        
        # Describe encounter
        if dwarves_present == 1:
            speak(4, messages)
        else:
            print(f"There are {dwarves_present} threatening little dwarves in the room with you!")
            print()
        
        # Handle attacks
        if attack_count > 0:
            if attack_count == 1:
                speak(5, messages)
                if hit_count > 0:
                    speak(52, messages)
                    print("\nGame over!")
                    sys.exit(0)
            else:
                print(f"{attack_count} of them throw knives at you!")
                print()
                if hit_count > 0:
                    if hit_count == 1:
                        speak(6, messages)
                    else:
                        print(f"{hit_count} of them get you!")
                        print()
                    print("Game over!")
                    sys.exit(0)
                else:
                    speak(7, messages)


def main():
    """Main entry point"""
    print("=" * 60)
    print("    COLOSSAL CAVE ADVENTURE")
    print("=" * 60)
    print()
    
    game = Adventure()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
