from leadanne2 import logger


def retry_on_exception(exception: type[Exception], tries=3):
    """
    Decorator that retries a function a specified number of times if a
    specific exception is raised.

    Args:
        exception (type[Exception]): The exception type to catch.
        tries (int, optional): The number of times to retry. Defaults to 3.

    Returns:
        function: The decorated function.

    Raises:
        exception: If the function fails after the specified number of tries.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(tries):
                try:
                    return func(*args, **kwargs)
                except exception as ex:
                    logger.error(f"Failed on try {i+1}/{tries}")
                    logger.exception(ex)
            raise exception(f"Failed after {tries} tries")

        return wrapper

    return decorator
