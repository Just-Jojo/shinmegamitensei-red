# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Dict, Tuple, Union

from redbot.core import Config

from ._types import UserOrMember


__all__: Final[Tuple[str, ...]] = ("MaccaBank",)


class MaccaBank:
    def __init__(self, config: Config):
        self._config = config

        # {USER_ID: MACCA}
        self.__cache: Dict[int, int] = {}

    async def get_user_amount(self, user: Union[UserOrMember, int]) -> int:
        if isinstance(user, int):
            user_id = user
        else:
            user_id = user.id
        maybe_cached = self.__cache.get(user_id)
        if maybe_cached:
            return maybe_cached
        del maybe_cached
        macca = await self._config.custom("MACCA_BANK", str(user_id))
        if TYPE_CHECKING:
            assert isinstance(macca, int)
        self.__cache[user_id] = macca
        return macca
