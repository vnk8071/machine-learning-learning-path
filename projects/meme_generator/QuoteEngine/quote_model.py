"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""


class QuoteModel:
    def __init__(
        self,
        body: str = "Work hard - Play hard",
        author: str = "KhoiVN"
    ):
        """
        Simple Quote Model for getting quote and author

        Args:
            body (str, optional): [description]. Defaults to "Work hard - Play hard".
            author (str, optional): [description]. Defaults to "KhoiVN".
        """
        self.body = body
        self.author = author

    @property
    def title(self) -> str:
        """Return combination of quote and author"""
        return f"\"{self.body}\" by " + self.author

    def __str__(self) -> str:
        """Return string representation of QuoteModel"""
        return f"QuoteModel: {self.title}"

    def __repr__(self) -> str:
        """Return representation of QuoteModel"""
        return f"QuoteModel(body={self.body}, author={self.author})"
