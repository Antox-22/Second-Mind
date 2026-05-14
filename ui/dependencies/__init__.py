from app.core.path import ROOT
from ui.api.dependencies import Api
import webview

html = ROOT / "ui" / "dependencies" / "index.html"

windows = webview.create_window(
    title = "Second Mind - Package Manager",
    min_size=(700, 400),
    js_api=Api(),
    frameless=True,
    easy_drag=True,
    resizable=False,
    url= "file://" + str(html)
)

def start_ui():
    webview.start(
        icon=ROOT / "assets" / "icons" / "icon.ico",
        debug=True
    )

start_ui()