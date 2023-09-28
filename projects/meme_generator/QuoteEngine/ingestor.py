"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

from typing import List

from QuoteEngine.base import IngestorInterface
from QuoteEngine.quote_model import QuoteModel
from QuoteEngine.csv_ingestor import IngestorCSV
from QuoteEngine.doc_ingestor import IngestorDOC
from QuoteEngine.text_ingestor import IngestorText
from QuoteEngine.pdf_ingestor import IngestorPDF
from src.logger import Logger


logger = Logger.get_logger(__name__)


class Ingestor(IngestorInterface):
    """Subclass of IngestorInterface for parsing all files."""

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse file and return list of QuoteModel objects.

        Args:
            path (str): path to the file.

        Returns:
            quotes_list (List[QuoteModel]): list of QuoteModel objects.
        """
        for ingestor in [IngestorText, IngestorDOC, IngestorCSV, IngestorPDF]:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
