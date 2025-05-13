# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Final, Tuple

from redbot.core import Config

from ._types import UserMemberOrInt

__all__: Final[Tuple[str, ...]] = ("MaccaBank",)


if TYPE_CHECKING:

    def _get_user_id(maybe_user: UserMemberOrInt) -> int: ...

else:

    def _get_user_id(maybe_user):
        return getattr(maybe_user, "id", maybe_user)


class Macca(int):
    def __str__(self) -> str:
        return f"ћ{super().__str__()}"

    def __repr__(self) -> str:
        return f"ћ{super().__repr__()}"


class MaccaBank:
    def __init__(self, config: Config):
        self._config = config

        # {USER_ID: MACCA}
        self.__cache: Dict[int, int] = {}

    async def get_user_amount(self, user: UserMemberOrInt) -> Macca:
        user_id = _get_user_id(user)
        maybe_cached = self.__cache.get(user_id)
        if maybe_cached:
            return Macca(maybe_cached)
        del maybe_cached

        macca = await self._config.custom("MACCA_BANK", str(user_id)).macca()
        if TYPE_CHECKING:
            assert isinstance(macca, int)

        self.__cache[user_id] = macca
        return Macca(macca)

    async def add_to_user(self, user: UserMemberOrInt, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot go below 0 Macca")
        user_id = _get_user_id(user)
        current_amount = await self.get_user_amount(user_id)
        macca = current_amount + amount
        await self.set_user_amount(user_id, macca)

    async def set_user_amount(self, user: UserMemberOrInt, amount: int) -> None:
        if amount < 0:
            amount = 0
        user_id = _get_user_id(user)
        await self._config.custom("MACCA_BANK", str(user_id)).macca.set(amount)
        self.__cache[user_id] = amount

    def __len__(self) -> int:
        return len(self.__cache)
