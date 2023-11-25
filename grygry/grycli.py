import json
from collections.abc import Callable
from importlib import resources as rso
from typing import Any

from .lib.grylib import Grygry


def read_parameters() -> dict[str, Any]:
    path = rso.files("grygry.lib") / "parameters.json"
    return json.loads(path.read_text(encoding="utf8"))


def gry_searcher(key: str) -> Callable:
    def searcher():
        parameters = read_parameters()
        grygry = Grygry(parameters["_default_"] | parameters[key])
        grygry.search()

    return searcher


def functions_generator() -> None:
    for key in read_parameters():
        if key == "_default_":
            continue
        globals()[f"gry{key}"] = gry_searcher(key)


def _list_functions() -> None:
    lines = []
    for key in read_parameters():
        if key.startswith("_"):
            continue
        lines.append(f'gry{key} = "grygry.grycli:gry{key}"')
    print("\n".join(sorted(lines)))


functions_generator()
