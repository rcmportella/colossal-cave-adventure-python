# Translation Notes: Fortran to Python

## Overview

This document describes how the original Fortran 77 code was translated to Python, maintaining the game logic while modernizing the code structure.

## Major Changes

### 1. Structure
- **Fortran**: Single monolithic file with GOTO statements and numbered labels
- **Python**: Object-oriented design with `Adventure` class, separated into modules:
  - `adventure.py` - Main game engine
  - `game_data.py` - Data constants and configurations
  - `utils.py` - Helper functions

### 2. Control Flow
- **Fortran**: Heavy use of GOTO and computed GOTO statements
- **Python**: Structured control flow with methods, loops, and conditionals

### 3. Data Structures
- **Fortran**: Arrays with numeric indices (IOBJ, IPLACE, PROP, etc.)
- **Python**: Dictionaries with descriptive keys for better readability

### 4. Variables

| Fortran Variable | Python Equivalent | Purpose |
|-----------------|-------------------|---------|
| `LOC` | `self.location` | Current location |
| `IPLACE(I)` | `self.object_place[obj_id]` | Object locations |
| `PROP(I)` | `self.object_props[obj_id]` | Object properties/states |
| `IFIXED(I)` | `self.fixed[obj_id]` | Fixed objects |
| `IDWARF` | `self.dwarf_stage` | Dwarf encounter stage |
| `DLOC(I)` | `self.dwarf_locations[i]` | Dwarf locations |
| `ABB(I)` | `self.location_abbrev[i]` | Location visit count |

### 5. Key Translations

#### Initialization (Lines 1-1107 in Fortran)
```fortran
SETUP=1
KEYS=1
LAMP=2
DO 1101 I=1,100
    IPLACE(I)=IPLT(I)
1101 CONTINUE
```

Becomes:
```python
KEYS = 1
LAMP = 2
self.object_place = initial_placements.copy()
```

#### Main Loop (Lines 1-8 in Fortran)
```fortran
1   CALL YES(65,1,0,YEA)
    L=1
    LOC=1
2   DO 73 I=1,3
```

Becomes:
```python
def run(self):
    if yes_no_question(65, 0, 0, messages):
        self.show_instructions()
    while True:
        self.turn()
```

#### Motion Handling (Lines 8-40 in Fortran)
```fortran
8   KK=KEY(LOC)
    IF(KK.EQ.0)GOTO 19
9   LL=TRAVEL(KK)
    IF(1.EQ.MOD(LL,1024))GOTO 10
```

Becomes:
```python
def do_motion(self, motion_code):
    if self.location in travel_table:
        if motion_code in travel_table[self.location]:
            new_loc = travel_table[self.location][motion_code]
```

#### Object Actions (Lines 9000+ in Fortran)
```fortran
9000 IF(JOBJ.EQ.18)GOTO 2009
     IF(IPLACE(JOBJ).NE.J) GOTO 5200
9001 IF(IFIXED(JOBJ).EQ.0)GOTO 9002
```

Becomes:
```python
def do_take(self, obj_code):
    if obj_code == 18:
        speak(54, messages)
        return False
    if self.fixed.get(obj_code, False):
        speak(25, messages)
        return False
```

### 6. Improvements

1. **Readability**: Named constants instead of magic numbers
2. **Modularity**: Separate functions for each action
3. **Error Handling**: Try/except for graceful EOF and interrupts
4. **Modern I/O**: Python's `input()` instead of Fortran's `ACCEPT`
5. **Random Numbers**: Python's `random` module instead of custom RAN function

### 7. Known Limitations

The Python translation is a simplified version focusing on core gameplay:

1. **Data Loading**: The Fortran version loaded text from external file "TEXT". The Python version has messages embedded in code.
2. **Complete Map**: Only partial location map implemented for demonstration
3. **Scoring**: Original scoring system not fully implemented
4. **Save/Load**: Not implemented in this version
5. **Full Vocabulary**: Subset of original vocabulary

### 8. Game Logic Preserved

Key game mechanics maintained:
- ✓ Location navigation
- ✓ Object manipulation (take, drop)
- ✓ Lamp lighting system
- ✓ Grate locking/unlocking
- ✓ Dwarf encounters and combat
- ✓ Special interactions (bird vs snake)
- ✓ Dark room mechanics
- ✓ Contextual hints

### 9. Running Comparisons

**Original Fortran:**
```bash
f77 77-03-11_adventure.f -o adventure
./adventure
```

**Python Translation:**
```bash
python3 adventure.py
# or
./adventure.py
```

## Code Metrics

| Metric | Fortran | Python |
|--------|---------|--------|
| Total Lines | ~728 | ~650 (split across 3 files) |
| Main Logic | 728 lines | 550 lines |
| Functions/Subroutines | 4 | ~25 methods |
| GOTO statements | ~50 | 0 |
| Files | 1 | 3 |

## Conclusion

The Python translation modernizes the code while preserving the essential gameplay of the original 1976 Colossal Cave Adventure. The object-oriented design makes the code more maintainable and extensible for future enhancements.
