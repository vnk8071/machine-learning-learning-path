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
    logger.info("Branch GIT - KhoiVN")

    logger.info("1. SHOW BRANCH: git branch")
    logger.info("2. CREATE BRANCH: git branch <branch_name>")
    logger.info("3. SWITCH BRANCH: git checkout <branch_name>")
    logger.info("4. PUSH BRANCH: git push origin <branch_name>")


if __name__ == "__main__":
    main()
