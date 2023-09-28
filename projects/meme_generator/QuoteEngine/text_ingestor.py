"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

from typing import List
from QuoteEngine.base import IngestorInterface
from QuoteEngine.quote_model import QuoteModel
from src.logger import Logger


logger = Logger.get_logger(__name__)


class IngestorText(IngestorInterface):
    """Subclass of IngestorInterface for parsing txt files."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse txt file using open() function

        Args:
            path (str): path to the txt file

        Returns:
            quotes_list (List[QuoteModel]): list of QuoteModel
        """
        logger.info(f'Parsing TXT file: {path}')

        try:
            _ = cls.can_ingest(path=path)
        except Exception:
            raise FileNotFoundError("IngestorText cannot ingest this file.")
        finally:
            logger.info("IngestorText can ingest this file.")

        quotes_list = []
        with open(file=path, mode='r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip('\x0c').strip('\n')
                if line:
                    data = line.split('-')
                    body, author = data[0].strip('" '), data[1].strip()
                    quote_item = QuoteModel(body=body, author=author)
                    quotes_list.append(quote_item)
        return quotes_list
