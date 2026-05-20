from app.core.log import log
import functools, json

def safe(message=None, retry=False, window=None, data={}, exception_data: dict={}):
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

                    if not window:
                        log.debug("Window not taken.")
                        return message

                    if e in exception_data:
                        error_msg = exception_data[e]
                        safe_data = json.dumps(data)
                        showError(window, error_msg, safe_data)
                    else:
                        safe_error_data = json.dumps({"error": str(e)})
                        showError(window, "unexpected_error", safe_error_data)

                return message
        return wrapper
    return decorator

def showError(window, message, data):
    if not window:
        log.exception(f"Unable to comunicato w/ frontend")
        return
    window.resize(800, 600)
    window.evaluate_js(f"window.showError('{message}', {data})")