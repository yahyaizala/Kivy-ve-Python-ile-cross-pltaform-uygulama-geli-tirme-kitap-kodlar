from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from jnius import autoclass
from android.runnable import run_on_ui_thread
WebView=autoclass("android.webkit.WebView")
WebClient=autoclass("android.webkit.WebViewClient")
activity=autoclass("org.renpy.android.PythonActivity").mActivity
class KBrowserLayout(RelativeLayout):
    @run_on_ui_thread
    def setBrowser(self,url):
        self.webview = WebView(activity)
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setUseWideViewPort(True)  # enables viewport assets meta tags
        settings.setLoadWithOverviewMode(True)  # uses viewport
        settings.setSupportZoom(True)  # enables zoom
        settings.setBuiltInZoomControls(True)  # enables zoom controls
        wvc = WebClient()
        settings.setAllowFileAccessFromFileURLs(True)
        settings.setAllowUniversalAccessFromFileURLs(True)
        self.webview.setWebViewClient(wvc)
        activity.setContentView(self.webview)
        self.webview.loadUrl(url)

class KBrowserApp(App):
    def build(self):
        from kivy.core.window import Window
        Window.bind(on_keyboard=self.hook_kb)
        return KBrowserLayout()
    def load_site(self):
        site=self.root.ids["url_to_go"].text
        if not "http" in site:
            site="http://"+site
        self.root.setBrowser(site)

    def hook_kb(self, win, key, *largs):
        if key == 27:
            if self.root.webview.canGoBack():
                self.root.webview.goBack()
            return True
        elif key in (282, 319):
            print "setting panel goster"
            return True
        return False


if __name__ == '__main__':
    KBrowserApp().run()