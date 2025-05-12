# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Final, List, Union, Tuple
from ._types import Self


__all__: Final[Tuple[str, str]] = ("Arcana", "Demon")

_DEFAULT_MOVES: Final[Dict[str, Dict[str, Union[int, str]]]] = {
    "what": {
        "cost": 0,
        "cost_type": "fp",
        "level": 0,
    },
}


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
        arcana: str,
        exp: int,
        macca: int,
        resistances: Dict[str, str],
        moves: Dict[str, Dict[str, Union[str, int]]],
        url: str,
    ):
        self.name = name
        self._arcana = Arcana(arcana)
        self.arcana = self._arcana.pretty_name

        self._stats = stats
        self.exp = exp
        self.macca = macca
        self._resistances = resistances
        res: List[Resistances] = []
        for resitance, actual in resistances.items():
            res.append(Resistances(name, ResistEnum(actual)))
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

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            data.pop("name", "None"),
            data.pop("stats", {}),
            data.pop("arcana", "NONE"),
            data.pop("exp", 0),
            data.pop("macca", 0),
            data.pop("resistances", {}),
            data.pop("moves", {}),
            data.pop("url", ""),
        )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "stats": self._stats,
            "arcana": self._arcana,
            "exp": self.exp,
            "macca": self.macca,
            "resistances": self._resistances,
            "moves": self._moves
        }
