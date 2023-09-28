"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

from abc import ABC, abstractmethod
from typing import List

from QuoteEngine.quote_model import QuoteModel


class IngestorInterface(ABC):
    """Abstract base class for deriving concrete ingestor classes.

    Attributes:
        allowed_extensions (List[str]): list of allowed extensions
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the file can be ingested

        Args:
            path (str): path to the file

        Returns:
            bool: True if the file can be ingested, False otherwise
        """
        extension = path.rsplit(".", 1)[-1]
        return extension in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the file and return a list of QuoteModel

        Args:
            path (str): path to the file

        Returns:
            List[QuoteModel]: list of QuoteModel
        """
        pass
