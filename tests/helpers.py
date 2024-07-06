from pathlib import Path


def get_description(id: int, ext: str) -> str:
    """
    Helper function to fetch and read the description
    saved in a file.
    """
    base = Path("tests/__mock_data__/descriptions/")
    file = base / f"{id}.{ext}"
    return file.read_text(encoding="utf-8")
