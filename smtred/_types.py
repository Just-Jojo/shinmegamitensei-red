# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Protocol, Tuple, TypeVar, Union

import discord
from discord.ext.commands import Context as DiscordContext
from redbot.core.commands import Context as RedContext

__all__: Final[Tuple[str, ...]] = ("Context", "Readable", "Self", "UserMemberOrInt")

_T_co = TypeVar("_T_co", covariant=True)


if TYPE_CHECKING:
    from discord.ext.commands._types import BotT

    Context = DiscordContext[BotT]

else:
    Context = RedContext


# This is for `_load_json`
# as `orjson.load` is not actually a method
class Readable(Protocol[_T_co]):
    def read(self, length: int = ..., /) -> _T_co: ...


# I don't wanna do a try except block every time I import Self
# as it'd make me have to put a `type:ignore`
import sys

if sys.version_info >= (3, 10):
    from typing import Self
else:
    from typing_extensions import Self


UserMemberOrInt = Union[discord.User, discord.Member, int]

del sys, discord  # Not for export
