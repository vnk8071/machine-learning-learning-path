"""
Project: Git Tutorial
Author: KhoiVN
Date: 30/09/2023
"""
try:
    from utils.logger import Logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from utils.logger import Logger


logger = Logger.get_logger(__name__)


def main():
    logger.info("Stash GIT - KhoiVN")

    logger.info("1. PULL BRANCH: git pull")
    logger.info("1. CHECKOUT BRANCH: git checkout <branch_name>")
    logger.info("2. STASH: git stash save")
    logger.info("3. PULL BRANCH: git pull")
    logger.info("============")
    logger.info("4. POP STASH: git stash pop")
    logger.info("or")
    logger.info("4. APPLY STASH: git stash apply")
    logger.info("============")
    logger.info("5. COMMIT: git commit -m <message>")


if __name__ == "__main__":
    main()
