from decimal import Decimal
from msilib.schema import ComboBox
import os
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QMessageBox
from add_qty import Ui_Form
from encrypted import Connection
from decimal import Decimal


class AddItem(QMainWindow, Ui_Form, Connection):
    def __init__(self, parent=None):
        super(AddItem, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connector()
        self.setWindowTitle('إضافة صنف')
        self.get_all_stocks()
        self.handle_lines()


    def handle_lines(self):
        self.label_3.setVisible(False)
        self.lineEdit.editingFinished.connect(self.get_stock)
        self.pushButton.clicked.connect(self.save_close)
        self.pushButton_2.clicked.connect(self.save_add_new)
        self.pushButton_3.clicked.connect(self.close_window)


    def close_window(self):
        print('close Window')
        self.close()
    
    def save_close(self):
        self.update_item_information()
        self.close()

    def save_add_new(self):
        self.update_item_information()
        self.lineEdit.clear()
        self.lineEdit_3.setText('0')
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.comboBox.clear()
        self.comboBox_2.clear()

    def get_stock(self):
        try:
            self.comboBox_2.clear()
            self.cr.execute('SELECT id,stock,itemCost , itemSellPrice FROM item WHERE name = %s or code = %s',(self.lineEdit.text(),self.lineEdit.text(),))
            stocks = self.cr.fetchone()
            print('stocks',stocks[1])
            self.label_3.setText(str(stocks[0]))
            self.lineEdit_4.setText(str(stocks[2]))
            self.lineEdit_5.setText(str(stocks[3]))
            self.comboBox_2.setCurrentText(str(stocks[1]))
            self.get_all_stocks()
            
            self.lineEdit_3.setFocus()
        except TypeError:
            pass

        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))

    def update_item_information(self):
        try:
            if self.lineEdit.text()=="" or self.lineEdit_3.text()=="":
                QMessageBox.warning(self, 'Warning', "رجاء استكمال البيانات")

            else :
                self.cr.execute('''UPDATE item SET count = count + %s , itemCost = %s, itemSellPrice = %s WHERE id= %s''',
                    (Decimal(self.lineEdit_3.text()),self.lineEdit_4.text(),self.lineEdit_5.text(), self.label_3.text(),))
                self.db.commit()
                print(f'inserted 2 to {self.lineEdit.text()} ')

            QMessageBox.about(self,'تحديث بيانات الصنف', 'تمت الاضافة بنجاح')
        except Exception as e:
            QMessageBox.warning(self, "update_item_information", str(e))
        
    def get_all_stocks(self):
        self.comboBox_2.clear()
        self.cr.execute('SELECT name FROM stock')
        stocks = self.cr.fetchall()
        for stock in stocks:
            self.comboBox_2.addItem(stock[0])            

def main():
    app = QApplication(sys.argv)
    window = AddItem()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
