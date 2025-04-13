from __future__ import annotations

import inspect

from docstring_parser.numpydoc import parse

from pyanilist import AniList, AsyncAniList


def test_anilist_get_media_docs() -> None:
    """[Async]AniList.get_media has a LOT of parameters, make sure the docstring stays in sync."""
    docstring_params = [param.arg_name for param in parse(inspect.getdoc(AniList.get_media)).params]  # type: ignore[arg-type]
    async_docstring_params = [param.arg_name for param in parse(inspect.getdoc(AsyncAniList.get_media)).params]  # type: ignore[arg-type]
    params = inspect.getargs(AniList.get_media.__code__).args[1:]  # exclude the first "self" param
    async_params = inspect.getargs(AsyncAniList.get_media.__code__).args[1:]  # exclude the first "self" param

    assert docstring_params == async_docstring_params == params == async_params


def test_anilist_get_all_media_docs() -> None:
    """[Async]AniList.get_all_media has a LOT of parameters, make sure the docstring stays in sync."""
    docstring_params = [param.arg_name for param in parse(inspect.getdoc(AniList.get_all_media)).params]  # type: ignore[arg-type]
    async_docstring_params = [param.arg_name for param in parse(inspect.getdoc(AsyncAniList.get_all_media)).params]  # type: ignore[arg-type]
    params = inspect.getargs(AniList.get_all_media.__code__).args[1:]  # exclude the first "self" param
    async_params = inspect.getargs(AsyncAniList.get_all_media.__code__).args[1:]  # exclude the first "self" param

    assert docstring_params == async_docstring_params == params == async_params
