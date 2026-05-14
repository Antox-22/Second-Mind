from app.core.path import ROOT
import webview

def start_ui(_js_api):
    html = ROOT / "ui" / "dependencies" / "index.html"
    windows = webview.create_window(
        title = "Second Mind - Package Manager",
        js_api = _js_api,
        min_size=(700, 400),
        frameless=True,
        easy_drag=True,
        resizable=False,
        url= "file://" + html
    )

    webview.start(
        args=(windows),
        icon=ROOT / "assets" / "icons" / "icon.ico"
    )

start_ui(None)