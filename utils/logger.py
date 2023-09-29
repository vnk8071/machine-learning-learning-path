import logging


class Logger:
    """Logger class."""

    @classmethod
    def get_logger(cls, name: str):
        """Logger factory function.

        Args:
            name (str): Name of the logger.

        Returns:
            Logger: Logger object.
        """
        logger = logging.getLogger(name=name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger


if __name__ == "__main__":
    logger = Logger.get_logger(__name__)
    logger.info("This is a info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is a error message")
    logger.critical("This is a critical message")
