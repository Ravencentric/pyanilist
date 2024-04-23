<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    Simple AniList API wrapper to fetch media data
    <br/>
    <br/>
  </p>
</p>

<p align="center">
<a href="https://pypi.org/project/pyanilist/"><img src="https://img.shields.io/pypi/v/pyanilist" alt="PyPI - Version" ></a>
<img src="https://img.shields.io/pypi/pyversions/pyanilist" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/license/Ravencentric/pyanilist" alt="License">
<img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
</p>

<p align="center">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/test.yml?label=tests" alt="GitHub Workflow Status">
<a href="https://codecov.io/gh/Ravencentric/pyanilist"><img src="https://codecov.io/gh/Ravencentric/pyanilist/graph/badge.svg?token=B45ODO7TEY" alt="Codecov"></a>
</p>


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

PyAniList offers two main classes:

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

## License

Distributed under the [Unlicense](https://choosealicense.com/licenses/unlicense/) License. See [UNLICENSE](https://github.com/Ravencentric/pyanilist/blob/main/UNLICENSE) for more information.