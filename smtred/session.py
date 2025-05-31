"""
Session for SMT - Red

This cog uses SMT3's press turn system instead of Persona's combat system
Meaning we will have to store the amount of turns and update them whenver:
    - party member misses (I think this takes 2 turns?)
    - a party member hits a crit/weakness (this gives... 1/2 turns?)
    - a party member passes (I think this takes 1/2 turns)

This gives more control to the user for attacking/buffing/debuffing
"""

# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import Optional

import discord
from redbot.core import commands

from .demons import Demon, Party

__all__ = ("AlreadyRunning", "NotRunning", "Session")


class AlreadyRunning(Exception):
    """Gets raised when a session is already active"""

    pass


class NotRunning(RuntimeError):
    """Gets raised when trying to call functions that need the session started"""

    pass


class Session:
    def __init__(
        self,
        user: discord.User,
        player_party: Party,
        enemy_party: Party,
        ctx: commands.Context,
    ):
        self.user = user
        self.player_party = player_party
        self.enemy_party = enemy_party
        self.ctx = ctx

        self._message: Optional[discord.Message] = None
        self.current_demon: Demon
        if (p_demon := self.player_party.current_demon).higher_agility(
            e_demon := self.enemy_party.current_demon
        ):
            self.current_demon = p_demon
        else:
            self.current_demon = e_demon

    async def start(self, ctx: commands.Context) -> None:
        if self._message:
            raise AlreadyRunning
        ...
