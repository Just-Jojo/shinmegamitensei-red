# Copyright (c) 2025 - Amy (jojo7791)
# Licensed under MIT

from __future__ import annotations

from typing import TYPE_CHECKING

__all__ = ("load_json",)


try:
    import orjson

    if TYPE_CHECKING:
        from typing import Any

        from ._types import Readable

    # NOTE I think orjson gets installed with red, but I'm not sure

    def load_json(fp: Readable, *args, **kwargs) -> Any:
        return orjson.loads(fp.read(), *args, **kwargs)

except ModuleNotFoundError:
    import json

    load_json = json.load
