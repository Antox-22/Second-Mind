from app.core.log import log
import functools, json

window = None

def set_window(_window):
    global window
    window = _window

def safe(message=None, retry=False, _window=None, data={}, exception_data: dict={}):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            active_window = _window
            try:
                return func(*args, **kwargs)
            except Exception as e:

                # ERROR: Log the exception with the function name
                log.exception(f"Errore in {func.__name__} {"ReTry" if retry else ""}")

                try:
                    kwargs["was_error"] = True
                    kwargs["exception"] = e
                    return func(*args, **kwargs)
                except Exception as inner_e:

                    # ERROR: Log the exception with the function name
                    log.exception(f"Errore in {func.__name__}")
                    e = inner_e # Aggiorniamo l'eccezione con quella del secondo fallimento

                    if not active_window:
                        log.debug("Window not taken.")

                        global_window = globals().get('window', None)
                        if global_window:
                            active_window = global_window
                        else: return message


                    error_key = None
                    if type(e) in exception_data:
                        error_key = exception_data[type(e)]
                    elif str(e) in exception_data:
                        error_key = exception_data[str(e)]

                    if error_key:
                        showError(active_window, error_key, data)
                    else:
                        showError(active_window, "unexpected_error", {"error": str(e)})

                return message
        return wrapper
    return decorator

def showError(_window, message, data={}):
    if not _window:
        log.exception(f"Unable to comunicato w/ frontend")
        if window: _window = window
        else: return message

    _window.resize(800, 600)
    _window.evaluate_js(f"window.showError('{message}', {json.dumps(data)})")