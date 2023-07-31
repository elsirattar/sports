"""
print barcode module
"""
import sys

from PyQt5 import QtGui, QtWidgets, QtPrintSupport

from PIL import Image
from PIL.ImageQt import ImageQt


def handle_paint_request(printer, image_):
    printer.setOrientation(QtPrintSupport.QPrinter.Portrait)
    printer.setFullPage(False)
    printer.setPageMargins(0, 0, 0, 0, QtPrintSupport.QPrinter.Millimeter)

    image_ = ImageQt(image_).copy()

    painter = QtGui.QPainter(printer)
    image = QtGui.QPixmap.fromImage(image_)
    painter.drawPixmap(0, 0, image)
    painter.end()


class Print_barcode:
    def __init__(self, image_):
        printer = QtPrintSupport.QPrinter()
        dialog = QtPrintSupport.QPrintDialog(printer)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            handle_paint_request(printer, image_)


def do_print(image_):
    app = QtWidgets.QApplication(sys.argv)
    gui = Print_barcode(image_)


if __name__ == "__main__":
    im = Image.open("barcode.png", encoding="utf8").convert("RGB")
    do_print(im)
