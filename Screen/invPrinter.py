import sys
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QWidget,
                             QApplication, QVBoxLayout, QMessageBox)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtPrintSupport
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
import os
from PyQt5 import QtCore
from PyQt5.QtGui import *
import time


class PrintRecipt(QWidget):
    def __init__(self, parent=None):
        super(PrintRecipt, self).__init__()

        self.initUI()
        self.resize(360, 600)
        self.setWindowIcon(QIcon('awgLogo.ico'))

    def initUI(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        self.webEngineView = QWebEngineView()
        expBtn = QPushButton('طباعة', self)
        expBtn.clicked.connect(self.print_widget)
        hbox.addWidget(expBtn)
        vbox.addWidget(self.webEngineView)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setGeometry(0, 50, 350, 50)
        self.setWindowTitle('طباعة فاتورة')

        self.webEngineView.load(
            QtCore.QUrl.fromLocalFile(os.path.abspath(os.path.dirname(__file__)) + "/" + "invoice.html"))
        # self.webEngineView.loadFinished.connect(self.print_widget)

    def print_widget(self):
        print("print_widget working")
        self._printer = QtPrintSupport.QPrinter()
        QPrinter.setResolution(self._printer, 800)
        self.webEngineView.page().print(self._printer, self.printResult)

    def printResult(self, success):
        if success:
            print("done")
        else:
            print("print error")
        del self._printer


def main():
    app = QApplication(sys.argv)
    window = PrintRecipt()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
