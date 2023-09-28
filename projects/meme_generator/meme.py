import os
import random

from MemeEngine.generator import MemeGenerator
from QuoteEngine.ingestor import Ingestor
from src.logger import Logger


logger = Logger.get_logger(__name__)


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    meme = MemeGenerator(output_dir=args.output_dir)
    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        path = random.choice(imgs)

    try:
        if body is None and author is None:
            quote_files = [
                './_data/DogQuotes/DogQuotesTXT.txt',
                './_data/DogQuotes/DogQuotesDOCX.docx',
                './_data/DogQuotes/DogQuotesPDF.pdf',
                './_data/DogQuotes/DogQuotesCSV.csv'
            ]
            quotes = []
            for quote_file in quote_files:
                quotes.extend(Ingestor.parse(path=quote_file))

            quote = random.choice(quotes)
            path = meme.make_meme(
                img_path=path,
                text=quote.body,
                author=quote.author)
        else:
            path = meme.make_meme(img_path=path, text=body, author=author)
        return path
    except Exception:
        raise FileNotFoundError("Quotes not found.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create a meme')
    parser.add_argument(
        '-p', '--path',
        default="_data/photos/dog/xander_1.jpg",
        help='path to an image file'
    )
    parser.add_argument(
        '-b', '--body', type=str,
        help='quote body to add to the image'
    )
    parser.add_argument(
        '-a', '--author', type=str,
        help='quote author to add to the image'
    )
    parser.add_argument(
        '-o', '--output_dir', type=str,
        default="output",
        help='path to the directory to save meme'
    )
    args = parser.parse_args()
    generate_meme(path=args.path, body=args.body, author=args.author)
