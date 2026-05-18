from app.core.path import ROOT
from ui.api.dependencies import Api, set_window
import webview


html = ROOT / "ui" / "dependencies" / "index.html"

window = webview.create_window(
    title = "Second Mind - Package Manager",
    js_api=Api(),
    width=500,
    height=300,
    frameless=True,
    easy_drag=True,
    resizable=False,
    url= "file://" + str(html)
)

def start_ui():
    webview.start(
        func=set_window,
        args=(window,),
        icon=ROOT / "assets" / "icons" / "icon.ico",
        debug=True
    )

if __name__ == "__main__":
    start_ui()