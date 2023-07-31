from PyQt5.QtWidgets import *


class FetchTables:
    def __init__(self, tasks, table):
        self.tasks = tasks
        self.table = table
        self.fetch_data()

    def fetch_data(self):
        for row, form in enumerate(self.tasks):
            self.table.insertRow(row)
            for col, item in enumerate(form):
                self.table.setItem(row, col, QTableWidgetItem(str(item)))
