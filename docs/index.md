<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    Simple read-only Anilist API wrapper
    <br/>
    <br/>
  </p>
</p>

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/pyanilist?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyanilist%2F)](https://pypi.org/project/pyanilist/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyanilist)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/release.yml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/pyanilist/test.yml?label=tests&link=https%3A%2F%2Fgithub.com%2FRavencentric%2Fpyanilist%2Factions%2Fworkflows%2Ftest.yml)
![License](https://img.shields.io/github/license/Ravencentric/pyanilist)
![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

</div>


## About

- Supports both sync and async. 
- Read-only API wrapper.
- Only supports querying the `Media` type.

## Installation

`pyanilist` is available on [PyPI](https://pypi.org/project/pyanilist/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install pyanilist
```

## Usage

PyAnilist offers two main classes:

1. `Anilist()` - Synchronous class
    - `search()` - Search a media

        ```py
        >>> from pyanilist import Anilist, MediaType
        >>> media = Anilist().search("Attack on Titan", type=MediaType.ANIME)
        >>> media.title
        MediaTitle(romaji='Shingeki no Kyojin', english='Attack on Titan', native='進撃の巨人')
        >>> media.title.romaji
        'Shingeki no Kyojin'
        >>> media.site_url
        Url('https://anilist.co/anime/16498')
        >>> media.episodes
        25
        ```
    - `get()` - Get a media by it's Anilist ID

        ```py
        >>> from pyanilist import Anilist
        >>> media = Anilist().get(21459)
        >>> media.title
        MediaTitle(romaji='Boku no Hero Academia', english='My Hero Academia', native='僕のヒーローアカデミア')
        >>> media.title.english
        'My Hero Academia'
        >>> media.site_url
        Url('https://anilist.co/anime/21459')
        >>> media.episodes
        13
        ```

2. `AsyncAnilist()` - Asynchronous class
    - `search()` - Search a media

        ```py
        >>> import asyncio
        >>> from pyanilist import AsyncAnilist, MediaType
        >>> media = asyncio.run(AsyncAnilist().search("Attack on Titan", type=MediaType.ANIME))
        >>> media.title
        MediaTitle(romaji='Shingeki no Kyojin', english='Attack on Titan', native='進撃の巨人')
        >>> media.title.romaji
        'Shingeki no Kyojin'
        >>> media.site_url
        Url('https://anilist.co/anime/16498')
        >>> media.episodes
        25
        ```
    - `get()` - Get a media by it's Anilist ID

        ```py
        >>> import asyncio
        >>> from pyanilist import AsyncAnilist
        >>> media = asyncio.run(AsyncAnilist().get(21459))
        >>> media.title
        MediaTitle(romaji='Boku no Hero Academia', english='My Hero Academia', native='僕のヒーローアカデミア')
        >>> media.title.english
        'My Hero Academia'
        >>> media.site_url
        Url('https://anilist.co/anime/21459')
        >>> media.episodes
        13
        ```

## API Reference

Checkout the complete API reference [here](https://ravencentric.github.io/pyanilist/).

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pyanilist/blob/main/UNLICENSE) for more information.