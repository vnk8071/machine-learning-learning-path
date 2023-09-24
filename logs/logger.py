import logging
import datetime

DATETIME = datetime.datetime.now().strftime('%Y-%m-%d')


def get_logger(name: str):
    """
    Returns a logger object with the given name.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('logs/{}.log'.format(DATETIME))
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
