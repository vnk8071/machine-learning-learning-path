import random
import os
import requests
import tempfile
from flask import Flask, render_template, request

from MemeEngine.generator import MemeGenerator
from QuoteEngine.ingestor import Ingestor
from src.logger import Logger
from src.utils import get_current_timestamp


logger = Logger.get_logger(__name__)

app = Flask(__name__)

meme = MemeGenerator(output_dir='./static')


def setup():
    """ Load all resources """

    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesPDF.pdf',
        './_data/DogQuotes/DogQuotesCSV.csv'
    ]

    quotes = []
    for quote_file in quote_files:
        quotes.extend(Ingestor.parse(quote_file))

    try:
        images_path = "./_data/photos/dog/"
        for root, dirs, files in os.walk(images_path):
            imgs = [os.path.join(root, name) for name in files]
    except Exception:
        raise FileNotFoundError("Images not found.")

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)

    quote = random.choice(quotes)
    quote.body = quote.body.replace('\ufeff', '').replace('\u2019', "'")

    path = meme.make_meme(img_path=img, text=quote.body, author=quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    if image_url != '':
        response = requests.get(image_url)

        img = f'{tempfile.gettempdir()}/' + get_current_timestamp() + '.jpeg'
        with open(img, 'wb') as out:
            out.write(response.content)
    else:
        img = random.choice(imgs)

    if not body:
        body = random.choice(quotes).body

    if not author:
        author = random.choice(quotes).author

    path = meme.make_meme(img_path=img, text=body, author=author)

    if image_url != '':
        os.remove(img)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
