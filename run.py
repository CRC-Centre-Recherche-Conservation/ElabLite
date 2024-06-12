import sys
import atexit
import subprocess as sp
import os

from PySide6 import QtCore, QtWebEngineCore, QtWebEngineWidgets, QtWidgets


class CustomWebEnginePage(QtWebEngineCore.QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.profile().downloadRequested.connect(self.on_download_requested)

    @QtCore.Slot(QtWebEngineCore.QWebEngineDownloadRequest)
    def on_download_requested(self, download_item):
        filename = download_item.suggestedFileName()
        path = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", filename)[0]
        if path:
            download_item.setDownloadFileName(path)
            download_item.accept()
        else:
            download_item.cancel()


def kill_server(p):
    sp.run(['streamlit', 'cache', 'clear'], stdout=sp.DEVNULL)
    if os.name == 'nt':
        sp.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])
    elif os.name == 'posix':
        p.kill()


if __name__ == '__main__':
    cmd = f'streamlit run app.py --server.headless=True'

    p = sp.Popen(cmd.split(), stdout=sp.DEVNULL)
    atexit.register(kill_server, p)

    hostname = 'localhost'
    port = 8501

    app = QtWidgets.QApplication(sys.argv)
    view = QtWebEngineWidgets.QWebEngineView()
    custom_page = CustomWebEnginePage()
    view.setPage(custom_page)

    view.load(QtCore.QUrl(f'http://{hostname}:{port}'))
    view.show()
    sys.exit(app.exec())
