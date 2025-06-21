import functools
import pickle
from pathlib import Path
import logging
from typing import Any, Callable, Optional
import time

logger = logging.getLogger(__name__)

def disk_cache(cache_path: str):
    """
    A decorator that caches the results of a function to disk.
    
    Args:
        cache_path (str): Path where the cache file will be stored
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_file = Path(cache_path)
            
            # Create cache directory if it doesn't exist
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate a cache key based on function arguments
            cache_key = pickle.dumps((args, kwargs))
            
            try:
                if cache_file.exists():
                    with open(cache_file, 'rb') as f:
                        cache = pickle.load(f)
                        if cache_key in cache:
                            logger.debug(f"Cache hit for {func.__name__}")
                            return cache[cache_key]
                else:
                    cache = {}
                
                # Cache miss, compute the result
                result = func(*args, **kwargs)
                
                # Store in cache
                cache[cache_key] = result
                with open(cache_file, 'wb') as f:
                    pickle.dump(cache, f)
                
                return result
            
            except Exception as e:
                logger.error(f"Cache error for {func.__name__}: {str(e)}")
                # If there's any cache error, just compute and return the result
                return func(*args, **kwargs)
                
        return wrapper
    return decorator

def measure_time(func: Callable) -> Callable:
    """
    A decorator that measures the execution time of a function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        logger.info(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute")
        return result
    
    return wrapper

class Memoize:
    """
    A memoization class that caches function results in memory.
    """
    def __init__(self, func: Callable):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in self.cache:
            self.cache[key] = self.func(*args, **kwargs)
        return self.cache[key]
    
    def clear_cache(self):
        """Clear the cache"""
        self.cache = {}
