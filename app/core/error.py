from app.core.log import log
import functools

def safe(message=None, retry=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:

                # ERROR: Log the exception with the function name
                log.exception(f"Errore in {func.__name__} {"ReTry" if retry else ""}")

                try:
                    kwargs["was_error"] = True
                    kwargs["exception"] = e
                    return func(*args, **kwargs)
                except Exception as e:

                    # ERROR: Log the exception with the function name
                    log.exception(f"Errore in {func.__name__}")

                return message
        return wrapper
    return decorator