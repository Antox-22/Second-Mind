from app.core.path import ROOT
import webview

def start_ui(_func, _js_api):
    windows = webview.create_window(
        title = "Second Mind - Package Manager",
        js_api = _js_api,
        min_size=(700, 400),
        frameless=True,
        easy_drag=True,
        resizable=False,

        # DEBUG: TEST URL
        url="https://example.org"
    )

    webview.start(
        func=_func,
        args=(windows),
        icon=ROOT / "assets" / "icons" / "icon.ico"
    )