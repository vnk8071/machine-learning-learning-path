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
    logger.info("Merge GIT - KhoiVN")

    logger.info("1. CHECKOUT BRANCH: git checkout <branch_target>")
    logger.info("2. MERGE BRANCH: git merge <branch_source>")
    logger.info("3. PUSH MERGE: git push origin <branch_target>")

    logger.info("===============")
    logger.info("If conflict:")
    logger.info("1. CHECKOUT BRANCH: git checkout <branch_target>")
    logger.info("2. MERGE BRANCH: git merge <branch_source>")
    logger.info("3. RESOLVE CONFLICT")


if __name__ == "__main__":
    main()
