<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/pyanilist">
    <img src="https://raw.githubusercontent.com/Ravencentric/pyanilist/main/docs/assets/logo.png" alt="Logo" width="400">
  </a>
  <p align="center">
    A Python wrapper for the AniList API
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
<img src="https://img.shields.io/github/actions/workflow/status/ravencentric/pyanilist/tests.yml?label=tests" alt="GitHub Workflow Status">
<a href="https://codecov.io/gh/Ravencentric/pyanilist"><img src="https://codecov.io/gh/Ravencentric/pyanilist/graph/badge.svg?token=B45ODO7TEY" alt="Codecov"></a>
</p>


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

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See [LICENSE](https://github.com/Ravencentric/pyanilist/blob/main/LICENSE) for more information.
