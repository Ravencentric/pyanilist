<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    Simple AniList API wrapper to fetch media data
  </p>
</p>

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/pyanilist?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyanilist%2F)](https://pypi.org/project/pyanilist/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyanilist)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/release.yml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/pyanilist/test.yml?label=tests)
![License](https://img.shields.io/github/license/Ravencentric/pyanilist)
![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

</div>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
* [Docs](#docs)
* [License](#license)

## About

- Supports both sync and async.
- Provides easy access to almost every field present in AniList's `Media` type.
- Only supports querying the `Media` type

## Installation

`pyanilist` is available on [PyPI](https://pypi.org/project/pyanilist/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install pyanilist
```

## Usage

1. `AniList()` - Synchronous class
    - `search()` - Search a media

        ```py
        from pyanilist import AniList, MediaType

        media = AniList().search("Attack on Titan", type=MediaType.ANIME)

        print(media.title.romaji)
        """
        Shingeki no Kyojin
        """
        print(media.site_url)
        """
        https://anilist.co/anime/16498
        """
        print(media.episodes)
        """
        25
        """
        ```
    - `get()` - Get a media by it's AniList ID

        ```py
        from pyanilist import AniList

        media = AniList().get(21459)

        print(media.title.english)
        """
        My Hero Academia
        """
        print(media.site_url)
        """
        https://anilist.co/anime/21459
        """
        print(media.episodes)
        """
        13
        """
        ```

2. `AsyncAniList()` - Asynchronous class
    - `search()` - Search a media

        ```py
        import asyncio
        from pyanilist import AsyncAniList, MediaType

        media = asyncio.run(AsyncAniList().search("Attack on Titan", type=MediaType.ANIME))

        print(media.title.romaji)
        """
        Shingeki no Kyojin
        """
        print(media.site_url)
        """
        https://anilist.co/anime/16498
        """
        print(media.episodes)
        """
        25
        """
        ```
    - `get()` - Get a media by it's AniList ID

        ```py
        import asyncio
        from pyanilist import AsyncAniList
        
        media = asyncio.run(AsyncAniList().get(21459))

        print(media.title.english)
        """
        My Hero Academia
        """
        print(media.site_url)
        """
        https://anilist.co/anime/21459
        """
        print(media.episodes)
        """
        13
        """
        ```

## Docs

Checkout the complete documentation [here](https://pyanilist.zip).

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pyanilist/blob/main/UNLICENSE) for more information.