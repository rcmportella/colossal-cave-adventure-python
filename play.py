#!/usr/bin/env python3
"""
Quick start guide for Colossal Cave Adventure
Demonstrates basic gameplay
"""

print("""
=================================================================
    COLOSSAL CAVE ADVENTURE - QUICK START GUIDE
=================================================================

BASIC COMMANDS:
--------------
Movement:    NORTH, SOUTH, EAST, WEST (or N, S, E, W)
             UP, DOWN, IN, OUT

Objects:     TAKE [object], DROP [object]
             INVENTORY (or I) - see what you're carrying

Actions:     LOOK (or L) - look around again
             LIGHT LAMP, EXTINGUISH LAMP
             UNLOCK GRATE, LOCK GRATE
             EAT FOOD, DRINK WATER
             ATTACK [creature]

Other:       QUIT - exit the game


GETTING STARTED:
---------------
1. You start at the end of a road
2. Go IN to the building
3. TAKE KEYS and TAKE LAMP
4. Come back OUT
5. Explore! Try going SOUTH, EAST, or into the FOREST


TIPS:
-----
- The lamp is essential for exploring dark areas
- Some areas require specific items or actions
- Watch out for dwarves in the deeper parts of the cave!
- Type commands in UPPER or lower case - both work
- You can use short forms: N for NORTH, I for INVENTORY, etc.


SAMPLE SESSION:
--------------
> IN
> TAKE KEYS
> TAKE LAMP
> OUT
> SOUTH
> WEST
> SOUTH
> DOWN
> LIGHT LAMP
> DOWN


Press Enter to start the game...
""")

input()

import adventure
adventure.main()
