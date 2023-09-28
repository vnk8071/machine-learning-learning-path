"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

from typing import List
from docx import Document
from QuoteEngine.base import IngestorInterface
from QuoteEngine.quote_model import QuoteModel
from src.logger import Logger


logger = Logger.get_logger(__name__)


class IngestorDOC(IngestorInterface):
    """Subclass of IngestorInterface for parsing csv files."""

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse csv file using pandas library

        Args:
            path (str): path to the csv file

        Returns:
            quotes_list (List[QuoteModel]): list of QuoteModel
        """
        logger.info(f'Parsing DOC file: {path}')

        try:
            _ = cls.can_ingest(path=path)
        except Exception:
            raise FileNotFoundError("IngestorDOC cannot ingest this file.")
        finally:
            logger.info("IngestorDOC can ingest this file.")

        quotes_list = []
        doc = Document(path)

        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if len(text) > 0:
                data = text.split('-')
                body, author = data[0].strip('" '), data[1].strip()
                new_quote = QuoteModel(body=body, author=author)
                quotes_list.append(new_quote)
        return quotes_list
