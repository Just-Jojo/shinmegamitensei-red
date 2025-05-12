# Copyright (c) 2021 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import Final, Protocol, Tuple, TypeVar

__all__: Final[Tuple[str, ...]] = ("Readable",)

_T_co = TypeVar("_T_co", covariant=True)


class Readable(Protocol[_T_co]):
    def read(self, length: int = ..., /) -> _T_co: ...  # noqa
