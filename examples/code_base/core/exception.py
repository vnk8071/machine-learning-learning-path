# Define exception classes for the core module.
from typing import Optional
import http


class CustomException(Exception):
    """Base class for custom exceptions."""

    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
        headers: Optional[dict] = None,
    ):
        """Initialize custom exception.

        Args:
            status_code (int): HTTP status code.
            detail (str, optional): Error message. Defaults to None.
            headers (dict, optional): HTTP headers. Defaults to None.
        """
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code} {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"


if __name__ == "__main__":
    exception = CustomException(
        status_code=200,
        detail="This is a custom exception"
    )
    print(exception)  # 200 This is a custom exception
