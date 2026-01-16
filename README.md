# Colossal Cave Adventure - Python Version

This is a Python translation of the original 1976 Colossal Cave Adventure game, originally written in Fortran 77.

## About

The original game was written by Will Crowther in 1976 and is considered the first text adventure game in video game history. This Python version maintains the gameplay and logic of the original while using modern Python programming practices.
The original Fortran source can be found in https://github.com/wh0am1-dev/adventure

## Requirements

- Python 3.6 or higher
- No external dependencies required

## How to Play

```bash
python adventure.py
```

## Game Commands

- **Movement**: NORTH, SOUTH, EAST, WEST, UP, DOWN, IN, OUT, etc.
- **Actions**: TAKE/CARRY, DROP, INVENTORY, LOCK, UNLOCK, LIGHT, EXTINGUISH
- **Attack**: ATTACK, THROW
- **Other**: EAT, DRINK, RUB, POUR, LOOK, QUIT

## Files

- `adventure.py` - Main game engine
- `game_data.py` - Game text, locations, and object definitions
- `utils.py` - Helper functions

## Original Source

Based on the original Fortran 77 source code from March 11, 1977.

## License

This is for educational purposes only, preserving a piece of gaming history.
