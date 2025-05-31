# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, Final, Tuple, Union

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path

from ._types import Context
from .constants import CONTRACT, __author__, __version__, config_structure
from .demons import Demon
from .macca import Macca, MaccaBank  # noqa
from .modals import Menu, Page, RegisterView  # noqa
from .utils import load_json

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

        self.config.init_custom("MACCA_BANK", 1)
        self.config.register_custom("MACCA_BANK", macca=0)

        self.macca_bank = MaccaBank(self.config)
        self._demons: Dict[str, Union[str, int]] = {}

        # Initalize demon list
        self._task = self.bot.loop.create_task(self.init())

    async def cog_unload(self) -> None:
        if self._task:
            self._task.cancel()

    def cog_check(self, ctx: Context) -> bool:
        return ctx.author.id == 544974305445019651
        # TODO (amy) uncomment this
        # if not ctx.guild:
        #     return True
        # return ctx.channel.permissions_for(ctx.me).embed_links

    def format_help_for_context(self, ctx: commands.Context) -> str:
        return (
            f"{super().format_help_for_context(ctx)}\n\n"
            f"**Author:**\t{__author__}\n"
            f"**Version:**\t{__version__}"
        )

    async def init(self) -> None:
        try:
            with open(bundled_data_path(self) / "demons.json") as fp:
                self._demons = load_json(fp)
        except Exception as e:
            log.debug("Couldn't open file", exc_info=e)

    @commands.group(name="shinmegamitensei", aliases=["smt"])
    async def shin_megami_tensei(self, ctx: commands.Context) -> None:
        """Play Shin Megami Tensei: Red"""
        pass

    @shin_megami_tensei.command(name="testdemon")
    async def test_demon(self, ctx: commands.Context, demon_name: str) -> None:
        demon = self._demons.get(demon_name)
        if not demon:
            await ctx.send("Can't find that demon, buddy")
            return
        demon["name"] = demon_name
        if TYPE_CHECKING:
            assert isinstance(demon, dict)
        dem = Demon.from_json(demon)
        await self.send_demon(ctx, dem)

    @shin_megami_tensei.command(name="register")
    async def smt_register(self, ctx: commands.Context) -> None:
        """Start a contract with Igor"""
        registered = await self.config.user(ctx.author).registered()
        if registered:
            first, last = registered
            actual = CONTRACT.format(rname=first, lname=last)
            await self.send(ctx, actual)
            return
        view = RegisterView(ctx)
        await view.start()
        await view.wait()
        first_name = view._first_name
        last_name = view._last_name
        await self.config.user(ctx.author).registered.set([first_name, last_name])
        await ctx.send(
            "Good. All signed and sealed. Now let's begin the transfusion. "
            "Oh, don't you worry. Whatever happens... You may think it all a mere bad dream..."
            "\n\nOh, and have some Macca, would you?\n-# Added ћ200 to your bank"
        )
        await self.macca_bank.set_user_amount(ctx.author, 200)

    @shin_megami_tensei.command(name="bank")
    async def smt_bank(self, ctx: commands.Context) -> None:
        """See the amount of Macca you have"""
        if not await self.config.user(ctx.author).registered():
            await ctx.send(f"You are not registered yet, use `{ctx.prefix}smt register`")
            return
        macca = await self.macca_bank.get_user_amount(ctx.author)
        await ctx.send(f"You have {macca}")

    async def send_demon(self, ctx: commands.Context, demon: Demon) -> None:
        if not await ctx.embed_requested():
            await ctx.send(
                f"# Demon {demon.name}\n\n"
                f"## Stats\n{demon._stats}\n\n"
                f"## Abilities\n{demon.abilities}\n\n"
                f"## Arcana\n{demon.arcana}\n\n"
                f"## Resistances\n{demon.resistances}"
            )
            return
        embed = discord.Embed(
            title=f"Demon {demon.name}",
            colour=await ctx.embed_colour(),
            description=demon.description,
        )
        embed.set_image(url=demon.url)
        embed.add_field(name="Stats", value=demon._stats)
        embed.add_field(name="Abilities", value=demon.abilities)
        embed.add_field(name="Arcana", value=demon.arcana)
        embed.add_field(name="Resistances", value=demon.resistances)
        await ctx.send(embed=embed)
