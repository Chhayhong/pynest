from fastapi import HTTPException
from functools import wraps
import logging

def handle_status_code_500_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"\033[91mAn error occurred: {e}\033[0m")
            raise HTTPException(status_code=500, detail="Internal Server Error") from None
    return wrapper