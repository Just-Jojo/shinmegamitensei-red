# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import Final

__all__ = ("config_structure", "__author__", "__version__", "CONTRACT")

config_structure: Final[dict] = {
    "demons": [],  # List[Demon]
    "items": [],  # TODO(Amy) maybe dict with types?
    "registered": [],  # Will be their name
    "stats": {
        "strength": 5,
        "magic": 5,
        "vitality": 5,
        "agility": 5,
        "luck": 5,
    },
    "finished": False,  # TODO (Amy) Story work :3
}

__author__: Final[str] = "Amy (jojo7791)"
__version__: Final[str] = "1.0.0.dev0"

CONTRACT: Final[
    str
] = """I swear to tell the truth, the whole truth, and nothing but the truth
Poke you in the eye, say what?

__**X** {rname}__\t\t__{lname}__
**First name**\t\t**Last name**
"""
