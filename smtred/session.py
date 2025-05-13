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


import discord

__all__ = ("Session",)


class Session:
    def __init__(self, user: discord.User):
        self.user = user
