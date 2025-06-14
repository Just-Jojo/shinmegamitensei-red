# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Final, Iterable, List, Optional, Tuple, Union, overload

import discord

from ._types import Self

__all__: Final[Tuple[str, ...]] = (
    "Abilities",
    "Arcana",
    "CostType",
    "Demon",
    "DemonNotFound",
    "Move",
)

# None of these *should* be used if I'm not silly
# But still gonna have them here just in case
_DEFAULT_MOVES: Final[Dict[str, Dict[str, Union[int, str]]]] = {
    "what": {
        "cost": 0,
        "cost_type": "fp",
        "level": 0,
    },
}
_DEFAULT_ABILITIES = {k: 5 for k in ("strength", "magic", "vitality", "agility", "luck")}


class DemonNotFound(RuntimeError):
    def __init__(self):
        super().__init__("Couldn't find a demon!")


class CostType(Enum):
    FP = "fp"
    HP = "hp"


@dataclass
class Move:
    name: str
    cost: int
    cost_type: CostType
    level: int


class Arcana(Enum):
    """The arcana is the means by which all is revealed"""

    FOOL = "FOOL"
    MAGICIAN = "MAGICIAN"
    HIGH_PRIESTESS = "HIGH_PRIESTESS"
    EMPRESS = "EMPRESS"
    EMPEROR = "EMPEROR"
    HIEROPHANT = "HIEROPHANT"
    LOVERS = "LOVERS"
    CHARIOT = "CHARIOTS"
    JUSTICE = "JUSTICE"
    HERMIT = "HERMIT"
    FORTUNE = "FORTUNE"
    STRENGTH = "STRENGTH"
    HANGED_MAN = "HANGED_MAN"
    DEATH = "DEATH"
    TEMPERANCE = "TEMPERANCE"
    DEVIL = "DEVIL"
    TOWER = "TOWER"
    STAR = "STAR"
    MOON = "MOON"
    SUN = "SUN"
    JUDGEMENT = "JUDGEMENT"
    WORLD = "WORLD"  # NOTE I don't this is used in SMT?
    NONE = "NONE"

    @property
    def pretty_name(self) -> str:
        if self.value is self.NONE:
            return "None..."
        name = self.name
        name = name.replace("_", " ")
        return " ".join(x.capitalize() for x in name.split(" "))


ROMAN_NUMERALS: Final[Dict[int, str]] = {
    10: "X",
    5: "V",
    1: "I",
}


def _to_rmn(num: int) -> str:
    result = ""
    for arabic, roman in ROMAN_NUMERALS.items():
        factor, num = divmod(num, arabic)
        result += roman * factor
    return result


@dataclass
class Abilities:
    strength: int = 5
    magic: int = 5
    vitality: int = 5
    agility: int = 5
    luck: int = 5


class ResistEnum(Enum):
    WEAK = "WEAK"
    STRONG = "STRONG"
    NULL = "NULL"
    NONE = "NONE"
    ABSORB = "ABSORB"


@dataclass
class Resistances:
    name: str
    type: ResistEnum


class Demon:
    def __init__(
        self,
        name: str,
        stats: Dict[str, Union[str, int]],
        abilities: Dict[str, int],
        arcana: str,
        exp: int,
        macca: int,
        resistances: Dict[str, str],
        moves: Dict[str, Dict[str, Union[str, int]]],
        url: str,
        description: str,
    ):
        self.name = name
        self.description = description
        self.url = url
        self._arcana = Arcana(arcana)
        self.arcana = self._arcana.pretty_name

        # We'll keep a backup of abilities for export
        # and then have the "public" be `Abilities`
        self._abilities = abilities
        self.abilities = Abilities(**abilities)

        self._stats = stats
        self.exp = exp
        self.macca = macca
        self._resistances = resistances
        res: List[Resistances] = []
        for resistance, actual in resistances.items():
            res.append(Resistances(resistance, ResistEnum(actual)))
        self.resistances = res

        self._moves = moves
        # This is for public access of the moves
        _moves: List[Move] = []
        for move_name, move_data in moves.items():
            _moves.append(
                Move(
                    move_name,
                    move_data["cost"],  # type:ignore
                    CostType(move_data["cost_type"]),
                    move_data["level"],  # type:ignore
                )
            )
        self.moves = _moves

    def higher_agility(self, other: Demon) -> bool:
        if not isinstance(other, Demon):
            raise TypeError(f"Expected Demon not {other.__class__!r}")
        # we'll default to the player's party if the agility is the same
        return other.abilities.agility <= self.abilities.agility

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            data.pop("name", "None"),
            data.pop("stats", {}),
            data.pop("abilities", {}),
            data.pop("arcana", "NONE"),
            data.pop("exp", 0),
            data.pop("macca", 0),
            data.pop("resistances", {}),
            data.pop("moves", {}),
            data.pop("url", ""),
            data.pop("description", "No description..."),
        )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "stats": self._stats,
            "abilities": self._abilities,
            "arcana": self._arcana,
            "exp": self.exp,
            "macca": self.macca,
            "resistances": self._resistances,
            "moves": self._moves,
            "url": self.url,
            "description": self.description,
        }


class Party:
    def __init__(self, user: discord.User, demons: Iterable[Demon]):
        self.user = user
        self._demons = demons
        self.current_demon = self._get_next_demon(True)
        self.turns = len(self._demons) + 1

    @overload
    def _get_next_demon(self) -> Demon: ...

    @overload
    def _get_next_demon(self, initial: bool = True) -> Demon: ...

    def _get_next_demon(self, initial: bool = False) -> Demon:
        hit: Optional[Demon] = None if initial else self.current_demon
        for demon in self._demons:
            if not hit:
                hit = demon
                continue
            if not hit.higher_agility(demon):
                continue
            hit = demon
        if not hit:
            raise DemonNotFound
        return hit

    def sorted(self, *, reversed: bool = False) -> Party:
        """Sorts demons by their agility stat"""
        return Party(
            self.user,
            sorted(self._demons, key=lambda demon: demon.abilities.agility, reverse=reversed),
        )
