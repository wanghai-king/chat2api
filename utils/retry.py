from utils.Logger import logger
from fastapi import HTTPException

from utils.config import retry_times


async def async_retry(func, *args, max_retries=retry_times, **kwargs):
    for attempt in range(max_retries + 1):
        try:
            result = await func(*args, **kwargs)
            return result
        except HTTPException as e:
            if attempt == max_retries:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            logger.info(f"Retry {attempt + 1} failed with status code {e.status_code}. Retrying...")


def retry(func, *args, max_retries=retry_times, **kwargs):
    for attempt in range(max_retries + 1):
        try:
            result = func(*args, **kwargs)
            return result
        except HTTPException as e:
            if attempt == max_retries:
                raise HTTPException(status_code=e.status_code, detail=e.detail)
            logger.info(f"Attempt {attempt + 1} failed with status code {e.status_code}. Retrying...")
