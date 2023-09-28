"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

import os
from typing import List
import tempfile
import subprocess
from QuoteEngine.base import IngestorInterface
from QuoteEngine.quote_model import QuoteModel
from src.utils import get_current_timestamp
from src.logger import Logger


logger = Logger.get_logger(__name__)


class IngestorPDF(IngestorInterface):
    """Subclass of IngestorInterface for parsing csv files."""

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse csv file using pandas library

        Args:
            path (str): path to the csv file

        Returns:
            quotes_list (List[QuoteModel]): list of QuoteModel
        """
        logger.info(f'Parsing PDF file: {path}')

        try:
            _ = cls.can_ingest(path=path)
        except Exception:
            raise FileNotFoundError("IngestorPDF cannot ingest this file.")
        finally:
            logger.info("IngestorPDF can ingest this file.")

        quotes_list = []
        outfile = f'{tempfile.gettempdir()}/{get_current_timestamp()}.txt'
        subprocess.run(['pdftotext', '-table', path, outfile])

        fp = open(outfile, 'r')

        for line in fp.readlines():
            line = line.strip('\n').strip('\x0c')
            if line:
                data = line.split('-')
                body, author = data[0].strip('" '), data[1].strip()
                new_quote = QuoteModel(body=body, author=author)
                quotes_list.append(new_quote)

        fp.close()
        os.remove(outfile)

        return quotes_list
