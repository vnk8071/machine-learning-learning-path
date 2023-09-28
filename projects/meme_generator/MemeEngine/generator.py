"""
Project: Meme Generator
Author: KhoiVN
Date: 28/09/2023
"""

import random
import os

from PIL import Image, ImageDraw, UnidentifiedImageError

from src.logger import Logger
from src.utils import get_current_timestamp

logger = Logger.get_logger(__name__)


class MemeGenerator:
    """Class for generating memes."""

    def __init__(self, output_dir: str):
        """Init MemeEngine with the path to the directory to save meme.

        Args:
            output_dir (str): path to the directory to save meme.
        """
        self.output_dir = output_dir

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Generate and saves a meme using provided arguments.

        Args:
            img_path (str): path to the image file.
            text (str): body of the quote.
            author (str): author's name.
            width (int): maximum width of the generated meme.

        Returns:
            Path of saved image to the generated meme.

        Raises:
            FileNotFoundError: Error if image file was not found at the img_path location.
            UnidentifiedImageError: Error if image type is not recognized.
            OSError: Error if the file was not able to be saved.
        """
        try:
            logger.info(f'Generating meme from image: {img_path}')
            img = Image.open(img_path)
        except FileNotFoundError:
            raise FileNotFoundError('File was not found')
        except UnidentifiedImageError:
            raise UnidentifiedImageError("Unknown image type")

        resized_img = img.resize(
            size=(
                width,
                width / img.width * img.height
            )
        )
        quote = f"{text} - {author}".encode(encoding='latin-1',
                                            errors='ignore')
        logger.info(f'Adding quote: {quote} to the image')

        draw_img = ImageDraw.Draw(im=resized_img)
        text_position = (
            random.randint(0, resized_img.width * 0.75),
            random.randint(0, resized_img.height * 0.75)
        )
        draw_img.text(
            xy=text_position,
            text=quote,
            fill=(255, 255, 255, 255),
        )

        output_img_path = os.path.join(
            self.output_dir,
            get_current_timestamp() + '.png'
        )

        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            resized_img.save(output_img_path)
            logger.info(f'Meme was saved to: {output_img_path}')
        except OSError:
            raise OSError('File was not able to be saved')

        return output_img_path
