# Basic structure for data

## Demons:
```json
"name": {
    "stats": {
        // stats
    },
    "arcana": "arcana",
    "exp": 0, // amount of exp for defeating
    "macca": 0, // pay out for beating them
    "resistences": {
        "phys": "WEAK | STRONG | NULL | NONE | ABSORB",
        "pierce": "WEAK | STRONG | NULL | NONE | ABSORB",
        "fire": "WEAK | STRONG | NULL | NONE | ABSORB",
        "ice": "WEAK | STRONG | NULL | NONE | ABSORB",
        "elec": "WEAK | STRONG | NULL | NONE | ABSORB",
        "wind": "WEAK | STRONG | NULL | NONE | ABSORB",
        "psy": "WEAK | STRONG | NULL | NONE | ABSORB",
        "nuke": "WEAK | STRONG | NULL | NONE | ABSORB",
        "light": "WEAK | STRONG | NULL | NONE | ABSORB",
        "dark": "WEAK | STRONG | NULL | NONE | ABSORB",
        "alimighty": "NONE | STRONG" // Strong will only be for boss demons
    },
    "moves": {
        "move": {
            "levl": 0, // The level for unlocking a move, 0 being inbuilt
            "cost": 0, // hp/sp cost for move
            "cost_type": "hp | fp" // whether to drain from Focus or Hit points
        }
    },
    "url": "url for the demon's picture" // Use P5 version where possible
}
```