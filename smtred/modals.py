# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

import contextlib
import datetime
import logging
from typing import TYPE_CHECKING, Dict, Final, List, Optional, Tuple, Union, overload

import discord
from discord.ui.button import button as button_dec
from redbot.core import commands

from ._types import Self
from .constants import CONTRACT

__all__: Final[tuple] = ("RegisterView", "Menu", "Page")


log = logging.getLogger("red.smtred.modals")
button_emojis: Final[Dict[Tuple[bool, bool], str]] = {
    (False, True): "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}",
    (False, False): "\N{BLACK LEFT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
    (True, False): "\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
    (True, True): "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}",
}


class BaseButton(discord.ui.Button):
    if TYPE_CHECKING:
        view: Menu

    def __init__(self, forward: bool, skip: bool, disabled: bool = False):
        super().__init__(
            style=discord.ButtonStyle.grey, emoji=button_emojis[(forward, skip)], disabled=disabled
        )
        self.forward = forward
        self.skip = skip

    async def callback(self, inter: discord.Interaction) -> None:
        if self.skip:
            page_num = 1 if self.forward else -1
        else:
            current_num = self.view.current_page
            page_num = current_num + 1 if self.forward else current_num - 1
        await self.view.show_checked_page(page_num)


class StopButton(discord.ui.Button):
    if TYPE_CHECKING:
        view: Menu

    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.red,
            emoji="\N{HEAVY MULTIPLICATION X}\N{VARIATION SELECTOR-16}",
            disabled=False,
        )

    async def callback(self, inter: discord.Interaction) -> None:
        self.view.stop()
        with contextlib.suppress(discord.Forbidden):
            await self.view.msg.delete()


@overload
def _gen_timestamp() -> datetime.datetime: ...


@overload
def _gen_timestamp(string: bool = True) -> str: ...


def _gen_timestamp(string: bool = False) -> Union[str, datetime.datetime]:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    if not string:
        return now
    ret = int(now.timestamp())
    return f"<t:{ret}:r>"


class Page:
    def __init__(
        self,
        ctx: commands.Context,
        data: List[str],
        *,
        title: Optional[str] = None,
        footer: Optional[str] = None,
    ):
        self.ctx = ctx
        self.data = data
        self.title = title
        self.footer = footer  # Feet

    async def format_page(self, item: str) -> Dict[str, Union[discord.Embed, str]]:
        if await self.ctx.embed_requested():
            embed = discord.Embed(
                colour=await self.ctx.embed_colour(),
                title=self.title,
                timestamp=_gen_timestamp(),
            )
            embed.set_footer(text=self.footer)
            return {"embed": embed}
        ret = item
        if self.title:
            ret = f"#{self.title}\n\n{ret}"
        footer = _gen_timestamp(True)
        if self.footer:
            footer = f"-# {self.footer} {footer}"
        else:
            footer = f"-# {footer}"
        ret += f"\n{footer}"
        return {"content": ret}

    @property
    def __len__(self):
        return self.data.__len__

    @__len__.setter
    def __len__(self, val, /) -> None:
        pass


class Menu(discord.ui.View):
    if TYPE_CHECKING:
        msg: discord.Message

    def __init__(self, ctx: commands.Context, source: Page, *, timeout: float = 100.0):
        self.ctx = ctx
        self.source = source
        self.current_page: int = 0
        super().__init__(timeout=timeout)

    def _add_buttons(self) -> None:
        if len(self.source) > 3:
            self.add_item(BaseButton(False, True))
        self.add_item(BaseButton(False, False))
        self.add_item(StopButton())
        self.add_item(BaseButton(True, False))
        if len(self.source) > 3:
            self.add_item(BaseButton(True, True))

    @classmethod
    async def start(cls, ctx: commands.Context, source: Page, *, timeout: float = 100.0) -> Self:
        self = cls(ctx, source, timeout=timeout)
        page = self.source.data[0]
        kwargs = await self.source.format_page(page)
        self.msg = await self.ctx.send(view=self, **kwargs)
        return self

    async def show_page(self, page_number: int) -> None:
        page = self.source.data[page_number]
        self.current_page = page_number
        kwargs = await self.source.format_page(page)
        await self.msg.edit(view=self, **kwargs)  # type:ignore

    async def show_checked_page(self, page_num: int) -> None:
        max_len = len(self.source)
        try:
            if max_len > page_num >= 0:
                await self.show_page(page_num)
            elif max_len <= page_num:
                await self.show_page(0)
            else:
                await self.show_page(max_len - 1)
        except IndexError:
            pass

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "You are not authorized to use this menu", ephemeral=True
            )
            return False
        return True


class RegisterView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=100.0)
        self.ctx = ctx
        self.msg: discord.Message
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None

    async def start(self) -> None:
        actual = CONTRACT.format(rname=" " * 10, lname=" " * 9)
        self.msg = await self.ctx.send(actual, view=self)

    async def interaction_check(self, inter: discord.Interaction):
        log.info(f"{inter.user = }")
        if inter.user.id != 544974305445019651:
            await inter.response.send_message("I will find you", ephemeral=True)
            return False
        return True

    @button_dec(label="Register", style=discord.ButtonStyle.blurple)
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        modal = RegisterModal(title="Sign the contract...")
        await interaction.response.send_modal(modal)
        await modal.wait()
        self._first_name = rn = modal.first_name.value or modal.first_name.placeholder
        self._last_name = ln = modal.last_name.value or modal.last_name.placeholder
        button.disabled = True
        if TYPE_CHECKING:
            assert rn is not None
            assert ln is not None
        if len(rn) < 10:
            rn += "".join(" " for _ in range(10 - len(rn)))
        if len(ln) < 10:
            ln += "".join(" " for _ in range(9 - len(rn)))
        await self.msg.edit(content=CONTRACT.format(rname=rn, lname=ln), view=self)
        self.stop()


class RegisterModal(discord.ui.Modal):
    first_name: discord.ui.TextInput = discord.ui.TextInput(
        label="Your first name...",
        placeholder="Kanako",
        required=False,
        min_length=2,
        max_length=25,
    )
    last_name: discord.ui.TextInput = discord.ui.TextInput(
        label="Your last name...",
        placeholder="Ishimaru",
        required=False,
        min_length=2,
        max_length=25,
    )

    async def on_submit(self, inter: discord.Interaction) -> None:
        await inter.response.defer()
