from PyQt5 import QtGui, QtWidgets

class Table(QtWidgets.QTableView):
    # leave to False for the default behavior (the next cell is the one at the
    # right of the current, or the first of the next row; when set to True it
    # will always go to the next row, while keeping the same column
    useNextRow = False

    def closeEditor(self, editor, hint):
        if hint == QtWidgets.QAbstractItemDelegate.SubmitModelCache:
            if self.useNextRow:
                super().closeEditor(editor, hint)
                current = self.currentIndex()
                newIndex = current.sibling(current.row() + 1, current.column())
                if newIndex.isValid():
                    self.setCurrentIndex(newIndex)
                    self.edit(newIndex)
                return
            else:
                hint = QtWidgets.QAbstractItemDelegate.EditNextItem
        super().closeEditor(editor, hint)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test = Table()
    test.show()
    model = QtGui.QStandardItemModel(10, 5)
    test.setModel(model)
    sys.exit(app.exec_())