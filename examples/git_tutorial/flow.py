"""
Project: Git Tutorial
Author: KhoiVN
Date: 29/09/2023
"""
try:
    from utils.logger import Logger
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from utils.logger import Logger


logger = Logger.get_logger(__name__)


def main():
    logger.info("Flow GIT - KhoiVN")

    logger.info("1. CLONE: git clone https://.git")
    logger.info("2. COPY BRANCH into LOCAL: git checkout -b <branch_name>")

    logger.info("3. ADD Staging: git add .")
    logger.info("4. COMMIT Staging: git commit -m 'message'")
    logger.info("5. PUSH Staging: git push origin master")


if __name__ == "__main__":
    main()
