from __future__ import annotations

import subprocess
from pathlib import Path

SUBS = {
    "AsyncAniList": "AniList",
    "async_anilist_client": "anilist_client",
    "https://www.python-httpx.org/api/#asyncclient": "https://www.python-httpx.org/api/#client",
    "AsyncClient": "Client",
    "AsyncIterator": "Iterator",
    "async def": "def",
    "async with": "with",
    "async for": "for",
    "await ": "",
    "aclose()": "close()",
    "__aenter__": "__enter__",
    "__aexit__": "__exit__",
}


def unasync_line(line: str) -> str:
    for original, replacement in SUBS.items():
        line = line.replace(original, replacement)
    return line


def unasync_file(file: Path, destination: Path) -> None:
    with file.open(encoding="utf-8", newline="") as infile:
        with destination.open("w", encoding="utf-8", newline="") as outfile:
            outfile.write(
                f"# This file is automatically generated from {file.as_posix()} using `scripts/unasync.py`.\n"
                "# Do not edit it by hand.\n"
            )
            for line in infile:
                outfile.write(unasync_line(line))


def fmt(file: Path) -> None:
    subprocess.run(("uv", "run", "ruff", "format", file), check=True, capture_output=True)
    subprocess.run(("uv", "run", "ruff", "check", file, "--fix"), check=True, capture_output=True)


def main() -> None:
    src = Path("src/pyanilist/_aclient.py")
    dst = Path("src/pyanilist/_client.py")
    unasync_file(src, dst)
    fmt(dst)

    src = Path("tests/test_async_anilist.py")
    dst = Path("tests/test_anilist.py")
    unasync_file(src, dst)
    fmt(dst)


if __name__ == "__main__":
    main()
