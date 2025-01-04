from functools import wraps
import os
from fastapi import HTTPException

QUERY_PARAM_LIMIT = int(os.getenv("MAX_QUERY_LIMIT"))
class QueryParamLimitError(Exception):
    pass

def max_limit_query():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            query_param = kwargs.get('limit', 0)
            if query_param > QUERY_PARAM_LIMIT:
                raise HTTPException(status_code=400, detail=f"Query parameter exceeds the limit of {QUERY_PARAM_LIMIT}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
