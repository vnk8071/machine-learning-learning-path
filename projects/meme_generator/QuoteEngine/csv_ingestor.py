"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

from typing import List
import pandas as pd
from QuoteEngine.base import IngestorInterface
from QuoteEngine.quote_model import QuoteModel
from src.logger import Logger


logger = Logger.get_logger(__name__)


class IngestorCSV(IngestorInterface):
    """Subclass of IngestorInterface for parsing csv files."""

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse csv file using pandas library

        Args:
            path (str): path to the csv file

        Returns:
            quotes_list (List[QuoteModel]): list of QuoteModel
        """
        logger.info(f'Parsing CSV file: {path}')

        try:
            _ = cls.can_ingest(path=path)
        except Exception:
            raise FileNotFoundError("IngestorCSV cannot ingest this file.")
        finally:
            logger.info("IngestorCSV can ingest this file.")

        quotes_list = []
        df = pd.read_csv(filepath_or_buffer=path, header=0)

        for _, item in df.iterrows():
            body, author = item['body'], item['author']
            quote_item = QuoteModel(body=body, author=author)
            quotes_list.append(quote_item)
        return quotes_list
