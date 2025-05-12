# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)
del get_end_user_data_statement

from .core import ShinMegamiTensei as ShinMegoonerTensei


async def setup(bot: Red) -> None:
    await bot.add_cog(ShinMegoonerTensei(bot))
