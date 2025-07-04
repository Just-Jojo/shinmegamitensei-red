# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)
del get_end_user_data_statement

from .constants import __author__, __version__
from .core import ShinMegamiTensei as ShinMegoonerTensei

__all__ = ("__author__", "__red_end_user_data_statement__", "__version__", "setup")


async def setup(bot: Red) -> None:
    await bot.add_cog(ShinMegoonerTensei(bot))
