from typing import Dict, Any
from fastapi import FastAPI

from core.config import settings
from src.logger import Logger
from src.utils import get_current_timestamp
from module.cache.redis import RedisCache

logger = Logger.get_logger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)
redis_client = RedisCache(redis_url=settings.REDIS_URL)


# Use decorator to register route
@app.get(path="/")
async def root() -> Dict[str, str]:
    """Router for root url.

    Returns:
        Dict[str, str]: A dictionary with message key.
    """
    logger.info("Request to root url")
    return {"message": "Hello World"}


@app.get(path="/cache")
async def get_cache() -> Dict[str, Any]:
    """Router for cache url.

    Args:
        key (str): Key to get value for.

    Returns:
        Dict[str, str]: A dictionary with message key.
    """
    logger.info("Request to cache url")
    cache_value = redis_client.get()
    return {"cache": cache_value}


@app.post(path="/cache")
async def add_cache():
    """Router for cache url.

    Returns:
        Dict[str, str]: A dictionary with message key.
    """
    value = get_current_timestamp() + " - " + "LOGIN"
    logger.info("Request to cache url")
    redis_client.add(value=value)
    return {"cache": "Added value to cache successfully"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000)
    logger.info("Start API")
