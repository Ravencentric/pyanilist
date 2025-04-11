from __future__ import annotations


class AnilistError(Exception):
    """Base class for Anilist API errors, containing a message and status code."""

    def __init__(self, *, message: str, status_code: int):
        self._message = message
        self._status_code = status_code
        super().__init__(message)

    @property
    def message(self) -> str:
        """The error message returned by the API."""
        return self._message

    @property
    def status_code(self) -> int:
        """The HTTP status code of the error response."""
        return self._status_code


class MediaNotFoundError(AnilistError):
    """Specific Anilist error raised when a requested media item is not found."""

    def __init__(self) -> None:
        super().__init__(message="Not Found.", status_code=404)


class RateLimitError(AnilistError):
    """Specific Anilist error raised when the API rate limit is exceeded."""

    def __init__(self, *, retry_after: int):
        self._retry_after = retry_after
        message = f"Too Many Requests. Please wait for {self.retry_after} seconds before your next request."
        super().__init__(message=message, status_code=429)

    @property
    def retry_after(self) -> int:
        """The number of seconds to wait before making another request."""
        return self._retry_after
