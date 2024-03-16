from ._compat import metadata


def _get_version() -> str:
    """
    Get the version of juicenet
    """
    try:
        return metadata.version("pyanilist")

    except metadata.PackageNotFoundError:
        return "0.0.0"