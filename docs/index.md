<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    Simple Anilist API wrapper to fetch data about Anime or Manga
    <br/>
    <br/>
  </p>
</p>

<p align="center">
<a href="https://pypi.org/project/pyanilist/"><img src="https://img.shields.io/pypi/v/pyanilist" alt="PyPI - Version" ></a>
<img src="https://img.shields.io/pypi/pyversions/pyanilist" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/test.yml?label=tests" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/license/Ravencentric/pyanilist" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
</p>


## About

- Supports both sync and async. 
- Read-only API wrapper.
- Only supports querying the `Anime` or `Manga` type.
    - *Technically, Anilist has more than just Anime or Manga but they simply lump all animation into their `Anime` type and all comics/text-based media into their `Manga` type. This means that something like a `Light Novel` also falls in the `Manga` type*

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
        from pyanilist import Anilist, MediaType

        media = Anilist().search("Attack on Titan", type=MediaType.ANIME)

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
    - `get()` - Get a media by it's Anilist ID

        ```py
        from pyanilist import Anilist

        media = Anilist().get(21459)

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

2. `AsyncAnilist()` - Asynchronous class
    - `search()` - Search a media

        ```py
        import asyncio
        from pyanilist import AsyncAnilist, MediaType

        media = asyncio.run(AsyncAnilist().search("Attack on Titan", type=MediaType.ANIME))

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
    - `get()` - Get a media by it's Anilist ID

        ```py
        import asyncio
        from pyanilist import AsyncAnilist

        media = asyncio.run(AsyncAnilist().get(21459))

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

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pyanilist/blob/main/UNLICENSE) for more information.