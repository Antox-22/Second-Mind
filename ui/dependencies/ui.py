from app.utils.path import ROOT
from app.utils.log import log
from ui.api.dependencies import Api, set_window
import webview


html = ROOT / "ui" / "dependencies" / "index.html"
api = Api()
window = webview.create_window(
    title = "Second Mind - Package Manager",
    js_api=api,
    width=450,
    height=200,
    frameless=True,
    easy_drag=True,
    resizable=False,
    url= "file://" + str(html),
    confirm_close=True
)

def start_ui():
    webview.start(
        func=set_window,
        args=(window,),
        icon=ROOT / "assets" / "icons" / "icon.ico",
        debug=True
    )


    return api.return_state