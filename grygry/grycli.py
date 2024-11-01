import json
from collections.abc import Callable
from importlib import resources as rso
from typing import Any

from .lib.grylib import Grygry


def read_parameters() -> dict[str, Any]:
    path = rso.files("grygry.lib") / "parameters.json"
    params = json.loads(path.read_text(encoding="utf8"))
    return params


def gry_searcher(key: str) -> Callable:
    def searcher():
        parameters = read_parameters()
        if key.endswith("00"):
            param = parameters["_default_"] | parameters[key[:-2]]
            param["path_only"] = True
        else:
            param = parameters["_default_"] | parameters[key]
        grygry = Grygry(param)
        grygry.search()

    return searcher


def functions_generator() -> None:
    for key in read_parameters():
        if key == "_default_":
            continue
        globals()[f"gry{key}"] = gry_searcher(key)
        if key[-1] in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
            continue
        globals()[f"gry{key}00"] = gry_searcher(f"{key}00")


def grygry_functions() -> None:
    def _list_functions():
        lines = ['grygry_functions = "grygry.grycli:grygry_functions"']
        for key in read_parameters():
            if key.startswith("_"):
                continue
            lines.append(f'gry{key} = "grygry.grycli:gry{key}"')
            if key[-1] in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}:
                continue
            lines.append(f'gry{key}00 = "grygry.grycli:gry{key}00"')
        return lines

    print("\n".join(_list_functions()))


functions_generator()
