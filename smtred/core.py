# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Final, Dict, List, Optional, Union, Tuple

import discord
from discord.utils import escape_markdown
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils.chat_formatting import underline

try:
    import orjson

    if TYPE_CHECKING:
        from ._types import Readable

    # NOTE I think orjson gets installed with red, but I'm not sure

    def _load_json(fp: Readable, *args, **kwargs):
        return orjson.loads(fp.read(), *args, **kwargs)

except ModuleNotFoundError:
    import json

    _load_json = json.load

from .constants import __author__, __version__, config_structure, contract
from .demons import Demon
from .modals import Menu, Page, RegisterView  # noqa


__all__: Final[Tuple[str]] = ("ShinMegamiTensei",)

log = logging.getLogger("red.jojocogs.smtred")


class ShinMegamiTensei(commands.Cog):
    """A mixture of Shin Megami Tensei and Persona

    Fight and recruit demons, win against foes, and kill god
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, force_registration=True)
        self.config.register_global(jack_frost_send=True)
        self.config.register_user(**config_structure)
        self._demons: Dict[str, Union[str, int]] = {}

        # For Jack Frost dialogue
        self._jacking_my_frost: bool = False

        # Initalize demon list
        self._task = self.bot.loop.create_task(self.init())

    async def cog_unload(self) -> None:
        if self._task:
            self._task.cancel()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        return (
            f"{super().format_help_for_context(ctx)}\n\n"
            f"**Author:**\t{__author__}\n"
            f"**Version:**\t{__version__}"
        )

    async def init(self) -> None:
        self._jacking_my_frost = await self.config.jack_frost_send()
        try:
            with open(bundled_data_path(self) / "demons.json") as fp:
                data = _load_json(fp)
                log.debug(f"{data = }")
                self._demons = data
        except Exception as e:
            log.debug("Couldn't open file", exc_info=e)

    @commands.group(name="shinmegamitensei", aliases=["smt"])
    async def shin_megami_tensei(self, ctx: commands.Context) -> None:
        pass

    @shin_megami_tensei.command(name="testdemon")
    async def test_demon(self, ctx: commands.Context, demon_name: str) -> None:
        demon = self._demons.get(demon_name)
        if not demon:
            await self.jacking_my_frost(ctx, "Can't find that demon, buddy")
            return
        if TYPE_CHECKING:
            assert isinstance(demon, dict)
        dem = Demon(demon)
        await self.jacking_my_frost(ctx, f"{dem.arcana}")

    @shin_megami_tensei.command(name="register")
    async def smt_register(self, ctx: commands.Context) -> None:
        """Start a contract with Igor"""
        registered = await self.config.user(ctx.author).registered()
        if registered:
            first, last = registered
            actual = contract.format(rname=underline(first), lname=underline(last))
            await self.send(ctx, actual)
            return
        view = RegisterView()
        actual = contract.format(rname=escape_markdown("_" * 10), lname=escape_markdown("_" * 9))
        await self.jacking_my_frost(ctx, contract, view=view)

    def cog_check(self, ctx: commands.Context) -> bool:  # type:ignore
        return ctx.author.id == 544974305445019651

    async def send(
        self, ctx: commands.Context, content: Optional[str] = None, **kwargs
    ) -> discord.Message:
        """Hee ho, send a message like jack frost!"""
        if not self._jacking_my_frost:
            return await ctx.send(content, **kwargs)
        if not content:
            return await ctx.send("Hee ho", **kwargs)
        new_content: List[str] = []
        last = False  # False = "hee", True = "ho"
        for part in content.split(". "):
            hee = "Hee" if last else "Ho"
            last = not last
            part += ". " + hee
            new_content.append(part)
        content = "Hee, " + ". ".join(new_content)
        return await ctx.send(content, **kwargs)

    @property
    def jacking_my_frost(self):
        return self.send

    @jacking_my_frost.setter
    def jacking_my_frost(self, *a, **kw) -> None:
        return
