from __future__ import annotations

import inspect

from docstring_parser.numpydoc import parse

from pyanilist import AniList


def test_anilist_get_media_docs() -> None:
    """AniList.get_media has a LOT of parameters, make sure the docstring stays in sync."""
    docstring_params = [param.arg_name for param in parse(inspect.getdoc(AniList.get_media)).params]  # type: ignore
    params = inspect.getargs(AniList.get_media.__code__).args[1:]  # exclude the first "self" param

    assert docstring_params == params
