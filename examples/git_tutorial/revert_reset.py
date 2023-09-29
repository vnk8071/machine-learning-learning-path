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
    logger.info("Revert GIT - KhoiVN")

    logger.info("1. SHOW LOG: git log")

    logger.info("===============")
    logger.info("[REVERT]")
    logger.info("2. REVERT to <commit_id>: git revert <commit_id>")
    logger.info("2. REVERT to previous commit: git revert HEAD~1")
    logger.info("===============")
    logger.info("3. COMMIT REVERT: git commit -m 'REVERT <commit_id>'")

    logger.info("[RESET] -> Not save in history log (Use for sensitive data)")
    logger.info("2. RESET to <commit_id>: git reset --hard <commit_id>")
    logger.info("2. RESET to previous commit: git reset --hard HEAD~1")
    logger.info("===============")
    logger.info("3. COMMIT RESET: git commit -m 'RESET <commit_id>'")

    logger.info("4. PUSH REVERT: git push origin <branch_name>")


if __name__ == "__main__":
    main()
