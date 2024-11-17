<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    A Python wrapper for the AniList API
  </p>
</p>

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/pyanilist?link=https%3A%2F%2Fpypi.org%2Fproject%2Fpyanilist%2F)](https://pypi.org/project/pyanilist/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyanilist)
![License](https://img.shields.io/github/license/Ravencentric/pyanilist)
![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/pyanilist/release.yml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/pyanilist/tests.yml?label=tests)
[![codecov](https://codecov.io/gh/Ravencentric/pyanilist/graph/badge.svg?token=B45ODO7TEY)](https://codecov.io/gh/Ravencentric/pyanilist)

</div>

## Table Of Contents

* [Installation](#installation)
* [Docs](#docs)
* [License](#license)

## Installation

`pyanilist` is available on [PyPI](https://pypi.org/project/pyanilist/), so you can simply use [pip](https://github.com/pypa/pip) to install it.

```sh
pip install pyanilist
```

## Usage

```py
from pyanilist import AniList

with AniList() as anilist:
    media = anilist.get_media("My Hero Academia")
    print(media.title.romaji)
    #> Boku no Hero Academia
    print(media.site_url)
    #> https://anilist.co/anime/21459
    print(media.episodes)
    #> 13
```

## Docs

Checkout the complete documentation [here](https://pyanilist.ravencentric.cc).

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See [LICENSE](https://github.com/Ravencentric/pyanilist/blob/main/LICENSE) for more information.
