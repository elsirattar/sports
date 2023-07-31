import math
import os
import sys
import json
from typing import Union, Any
from datetime import date, timedelta
from datetime import datetime
from decimal import Decimal
import pyqtgraph as pg
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QStringListModel
from PyQt5 import QtPrintSupport
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox, QCompleter
from xlsxwriter import *
from Screen import invPrinter
from initializeHtml import ShowHtml
from customers import customer
from design import Ui_mainWindow as Main_Window
from generateBarcode import Barcode_generator
from login import Ui_MainWindow as Login
from qr.dailySalesQr import QrDailySales
from qr.dashBoardQr import QrDashboard
from qr.filterQrExpense import GernerateCostsFilter
from qr import showFilterQr
from qr import showQr
from qr import showQrExpense
from qr import showReportQrCode
from fetchTables import FetchTables
from send_backup import SendBackup
from encrypted import Connection
from cryptography.fernet import Fernet
import uuid
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image
from exportsql import ExportBackUp

LastStateRole = QtCore.Qt.UserRole

data = []
all_items = []
sessions = []
groups_ = []
coaches = []

# Loging class
class Signing(QMainWindow, Login, Connection):
    def __init__(self, parent=None):
        super(Signing, self).__init__(parent)
        QMainWindow.__init__(self)
        self.display = None
        self.window2 = None
        self.setupUi(self)
        self.connector()
        self.setGeometry(500, 50, 400, 600)  # (left , up ,width , height)
        self.setFixedSize(400, 570)  # can't resize window
        self.lineEdit.setFocus()
        self.lineEdit.editingFinished.connect(self.change_to_password)
        self.pushButton.clicked.connect(self.sign_in)
        self.pushButton_2.clicked.connect(self.showPassword)

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_Return:
            self.sign_in()

    def change_to_password(self):
        self.lineEdit_2.setFocus()

    def sign_in(self):
        """
        :return: main function in class
        """

        try:
            # self.check_trial()
            self.cr.execute('SELECT User_name ,user_password FROM signup WHERE User_name LIKE %s AND user_password LIKE %s',
                            (self.lineEdit.text(),self.lineEdit_2.text(),))
            users = self.cr.fetchone()
            user = users[0]
            user_password = users[1]
            print(user, user_password)

            if self.lineEdit.text() == user and self.lineEdit_2.text() == str(users[1]):
                self.close()
                self.window2 = Main()
                self.window2.show()
                # self.window2.comboBox_7.clear()
                print('check permissions')

                self.cr.execute('SELECT reports ,add_user, invoice, first_name FROM signup WHERE User_name LIKE %s AND user_password LIKE %s',
                            (self.lineEdit.text(),self.lineEdit_2.text(),))

                user_permissions = self.cr.fetchone()
                self.window2.label_6.setText(user_permissions[3])
                print(user_permissions)
                if user_permissions[0] == 1:
                    self.window2.pushButton_68.setVisible(True)
                
                if user_permissions[1] == 1:
                    self.window2.pushButton_71.setVisible(True)
                
                if user_permissions[2] == 1:
                    self.window2.pushButton_74.setVisible(True)
                
            else:
                if self.lineEdit.text() != user or self.lineEdit_2.text() != user_password:
                    QMessageBox.warning(self, 'error', 'إسم المستخدم أو الرقم السرى غير صحيح')
        except Exception as e:
            QMessageBox.about(self, 'Error', str(e))
            print(e)

    def showPassword(self):
        """toggle password to text and text to password"""
        if self.homeSearchEdit.echoMode() == QLineEdit.EchoMode.Normal:
            self.homeSearchEdit.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            self.homeSearchEdit.setEchoMode(QLineEdit.EchoMode.Normal)


# class Main
class Main(QMainWindow, Main_Window, Connection):
    itemsSum: Union[Union[int, Decimal], Any]
    stockCount: object

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.window_expire = None
        self.display = None
        self.setupUi(self)
        self.connector()
        self.buttons_handle()
        self.hide_BTN()
        self.home_page()
        self.categories_in_main_window()
        self.show_clients_per_current_month()
        self.disable_btn()
        self.validator()
        self.handlePrint()
        self.run_when_open()

    def run_when_open(self):
        self.get_clients_from_db()
        self.get_category_item_from_database()
        self.get_coach_to_comboBox()
        self.dateEdit_2.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_7.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_8.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_9.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_10.setDateTime(QtCore.QDateTime.currentDateTime())

    def buttons_handle(self):
        self.pushButton_30.clicked.connect(self.deleteItem)
        self.pushButton_13.clicked.connect(self.categories_tab)
        self.confirmPrint_2.toggled.connect(self.printStat)
        self.cancelPrint_2.toggled.connect(self.printStat)
        self.tableWidget_12.cellChanged.connect(self.editcells)
        self.pushButton_32.clicked.connect(self.validate_finish_date)
        self.pushButton_6.clicked.connect(self.clients_tab)
        self.pushButton_14.clicked.connect(self.show_add_client_frame)
        self.pushButton_16.clicked.connect(self.add_client_to_db)
        # self.tableWidget_11.doubleClicked.connect(self.select_client_to_invoice)
        self.customer_lineEdit.textChanged.connect(self.search_customer_to_add_to_account)
        self.pushButton_21.clicked.connect(self.categories_tab)
        self.pushButton_2.clicked.connect(self.categories_tab)
        self.pushButton_35.clicked.connect(self.all_clients_tab)
        self.pushButton_17.clicked.connect(self.home_page)
        self.pushButton_18.clicked.connect(self.home_page)
        self.pushButton_33.clicked.connect(self.home_page)
        self.pushButton_50.clicked.connect(self.home_page)
        self.pushButton_20.clicked.connect(self.home_page)
        self.pushButton_67.clicked.connect(self.home_page)
        self.pushButton_75.clicked.connect(self.home_page)
        self.pushButton_77.clicked.connect(self.home_page)
        self.pushButton_78.clicked.connect(self.home_page)
        self.pushButton_11.clicked.connect(self.home_page)
        self.client_search.textChanged.connect(self.search_all_clients)
        self.coach_search.textChanged.connect(self.search_all_coach)  
        self.pushButton_36.clicked.connect(self.coaches_tab)
        self.pushButton_48.clicked.connect(self.show_add_coach_frame)
        self.pushButton_49.clicked.connect(self.close_coach_frame)
        self.pushButton_10.clicked.connect(self.all_categories_tab)
        self.pushButton_7.clicked.connect(self.add_category_to_db)
        self.pushButton_47.clicked.connect(self.add_coach_to_db)
        self.pushButton_29.clicked.connect(self.add_package_tab)
        self.comboBox_8.currentIndexChanged.connect(self.show_pakage_by_category)
        self.pushButton_15.clicked.connect(self.add_packages_to_db)
        self.pushButton_5.clicked.connect(self.daily_activities_tab)
        self.pushButton_61.clicked.connect(self.show_daily_sales)
        self.pushButton_60.clicked.connect(self.daily_expense)
        self.pushButton_22.clicked.connect(self.day_activities)
        self.pushButton_68.clicked.connect(self.reports_tab)
        self.pushButton_63.clicked.connect(self.reports_tab)
        self.pushButton_62.clicked.connect(self.all_daily_expense)
        self.pushButton_59.clicked.connect(self.all_activities)
        self.pushButton_8.clicked.connect(self.expenses_tab)
        self.pushButton_45.clicked.connect(self.expenses_tab)
        self.pushButton_24.clicked.connect(self.show_all_costs)
        self.pushButton_23.clicked.connect(self.add_cost_to_db)
        self.pushButton_12.clicked.connect(self.show_all_sales_)
        self.sales_search.textChanged.connect(self.search_show_all_sales_)
        self.pushButton_43.clicked.connect(self.clients_activities_tab)
        self.pushButton_3.clicked.connect(self.add_to_temp_activity)
        self.pushButton_4.clicked.connect(self.current_sessions_tab)
        self.tableWidget.doubleClicked.connect(self.from_temp_to_sessions)
        self.pushButton.clicked.connect(self.finish_session)
        self.pushButton_71.clicked.connect(self.add_user_tab)
        self.pushButton_74.clicked.connect(self.invoice_setup_tab)
        self.pushButton_19.clicked.connect(self.update_invoice_info)
        self.confirmAddUser.clicked.connect(self.signUp)
        self.tableWidget_15.doubleClicked.connect(self.handle_client_activity)
        self.pushButton_26.clicked.connect(self.between_dates_activities)
        self.pushButton_41.clicked.connect(self.filter_all_daily_expense)
        self.pushButton_44.clicked.connect(self.filter_show_all_daily_sales)
        self.customer_lineEdit_2.textChanged.connect(self.search_show_clients_per_current_month)
       
    def current_sessions_tab(self):
        self.tabWidget.setCurrentIndex(21)
        self.get_current_sessions()
    
    def get_current_sessions(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT invoice, trainer, category, coach, date, start FROM temp_activity')
        names = self.cr.fetchall()
        FetchTables(names, self.tableWidget)
        

    def show_add_client_frame(self):
        self.frame_38.setVisible(True)
    
    def show_add_coach_frame(self):
        self.frame_45.setVisible(True)
        self.get_category_item_from_database()

    def close_coach_frame(self):
        self.frame_45.setVisible(False)
        self.get_category_item_from_database()

    def add_coach_to_db(self):
        try:
            if self.lineEdit_4.text() == "" or self.lineEdit_5.text() =="":
                QMessageBox.about(self, "بيانات ناقصة", "برجاء استكمال البيانات ")
            elif self.comboBox_2.currentIndex() == 0:
                QMessageBox.about(self, "بيانات ناقصة", "برجاء اختيار التخصص لاتمام العملية ")
            else:
                self.cr.execute("INSERT INTO coach(name, phone, category) VALUES(%s, %s, %s)",(self.lineEdit_4.text(), self.lineEdit_5.text(), self.comboBox_2.currentText(),))
                self.db.commit()
                QMessageBox.about(self, "done", "coach added successfully")
                self.get_all_coaches_from_db()
                self.clear_after_add_coach()
                
        except Exception as e:
            QMessageBox.about(self, "add coach", e)

    def clear_after_add_coach(self):
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.comboBox_2.setCurrentIndex(0)

    def add_user_tab(self):
        self.tabWidget.setCurrentIndex(1)
        self.get_users()
    
    def invoice_setup_tab(self):
        self.tabWidget.setCurrentIndex(19)
        self.get_invoice_info()
    
    def get_invoice_info(self):
        self.cr.execute("SELECT name, phone, note1, note2 FROM info")
        info = self.cr.fetchone()
        self.label_130.setText(str(info[0]))
        self.lineEdit_47.setText(str(info[1]))
        self.lineEdit_45.setText(str(info[2]))
        self.lineEdit_46.setText(str(info[3]))

    def update_invoice_info(self):
        self.cr.execute("UPDATE info SET phone =%s , note1= %s, note2 = %s",(self.lineEdit_47.text(),self.lineEdit_45.text(),self.lineEdit_46.text(), ))
        self.db.commit()
        QMessageBox.about(self, "Done", "Informations updated successfully")

    def clients_activities_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.show_clients_per_current_month()

    def clients_tab(self):
        self.tabWidget.setCurrentIndex(5)

    def categories_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_9.setCurrentIndex(0)

    def home_page(self):
        self.tabWidget.setCurrentIndex(6)
        self.connector()
    
    def all_clients_tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.get_all_clients_from_db()
    
    def coaches_tab(self):
       self.tabWidget.setCurrentIndex(8)
       self.get_all_coaches_from_db()
       self.get_category_item_from_database()
    
    def all_categories_tab(self):
        self.tabWidget.setCurrentIndex(10)
        self.get_category_from_groups()


    def daily_activities_tab(self):
        self.tabWidget.setCurrentIndex(11)
        self.show_daily_sales()
    
    def expenses_tab(self):
        self.tabWidget.setCurrentIndex(13) 
        self.tabWidget_2.setCurrentIndex(1)
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_9.clear()
        self.lineEdit_10.clear()

    def daily_expense(self):
        self.tabWidget_5.setCurrentIndex(1)
        self.show_daily_expense()

    def all_daily_expense(self):
        self.tabWidget_7.setCurrentIndex(1)
        self.show_all_daily_expense()
    
    def day_activities(self):
        self.tabWidget_5.setCurrentIndex(2)
        self.show_day_activities()

    def all_activities(self):
        self.tabWidget_7.setCurrentIndex(2)
        self.show_all_activities()
    
    
    
    def show_day_activities(self):
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, trainer, category, start, coach FROM activity WHERE date = %s ',(date.today().strftime('%Y-%m-%d'),))
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_5)

    def show_all_activities(self):
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, trainer, category, start, coach, date FROM activity')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_9)

    def show_daily_sales(self):
        self.tabWidget_5.setCurrentIndex(0)
        self.tableWidget_22.setRowCount(0)
        self.tableWidget_22.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, phone, groups, price, finish FROM daily_sales WHERE start_date = %s ',(date.today().strftime('%Y-%m-%d'),))
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_22)
    
    def show_daily_expense(self):
        self.tableWidget_23.setRowCount(0)
        self.tableWidget_23.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, price, status FROM expense WHERE date = %s ',(date.today().strftime('%Y-%m-%d'),))
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_23)
    
    def show_all_daily_expense(self):
        self.tableWidget_27.setRowCount(0)
        self.tableWidget_27.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_27.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, price, status, date FROM expense ')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_27)

    def filter_all_daily_expense(self):
        self.tableWidget_27.setRowCount(0)
        self.tableWidget_27.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute(f'''SELECT id, name, price, status, date FROM expense WHERE date BETWEEN 
            '{self.dateEdit_7.date().toPyDate()}' AND '{self.dateEdit_8.date().toPyDate()}' ''')
        months = self.cr.fetchall()
        FetchTables(months, self.tableWidget_27)

    def add_package_tab(self):
        self.tabWidget.setCurrentIndex(13)
        self.add_package_setup()
        self.get_all_packages()

    def add_package_setup(self):
        self.comboBox_8.clear()
        self.comboBox_8.addItem("اختر الفئة المخصصة")
        self.cr.execute('SELECT name FROM groups ')
        stock_items = self.cr.fetchall()
        for stock in stock_items:
            self.comboBox_8.addItem(stock[0])
    
    def get_all_packages(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT groups, name, count, price FROM items ')
        items = self.cr.fetchall()
        sorted_list = sorted(items, key=lambda item: item[0])
        FetchTables(sorted_list, self.tableWidget_3)

    def show_pakage_by_category(self):
        try:
            if self.comboBox_8.currentIndex() == 0:
                self.get_all_packages()
            else:
                self.tableWidget_3.setRowCount(0)
                self.tableWidget_3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
                self.cr.execute('SELECT groups, name, count, price FROM items WHERE groups =%s ',(self.comboBox_8.currentText(),))
                names = self.cr.fetchall()
                FetchTables(names, self.tableWidget_3)

        except Exception as e:
            print(e)

    def add_packages_to_db(self):
        try:
            if self.comboBox_8.currentIndex() == 0:
                QMessageBox.about(self, "Warning", "الرجاء ادخال الفئة بشكل صحيح ")
            elif self.lineEdit_7.text() == "" or self.lineEdit_19.text() == "" or self.lineEdit_21.text() == "" :
                QMessageBox.about(self, "Warning", "الرجاء أكمل البيانات بشكل صحيح ")
            else:
                self.cr.execute('INSERT INTO items(name, count, price, groups) VALUES(%s, %s, %s, %s)',
                (self.lineEdit_7.text(), self.lineEdit_19.text(), self.lineEdit_21.text(), self.comboBox_8.currentText()))
                self.db.commit()
                QMessageBox.about(self, "Done", "تمت الاضافة بنجاح")
                self.show_pakage_by_category()
        except Exception as e:
            print(e)

    def reports_tab(self):
        self.tabWidget.setCurrentIndex(16)
        self.show_all_daily_sales()

    def show_all_daily_sales(self):
        self.tabWidget_7.setCurrentIndex(0)
        self.tableWidget_25.setRowCount(0)
        self.tableWidget_25.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, phone, groups, price, start_date, finish FROM daily_sales ')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_25)
    
    def filter_show_all_daily_sales(self):
        self.tableWidget_25.setRowCount(0)
        self.tableWidget_25.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute(f'''SELECT id, name, phone, groups, price, start_date, finish FROM daily_sales WHERE start_date BETWEEN 
            '{self.dateEdit_9.date().toPyDate()}' AND '{self.dateEdit_10.date().toPyDate()}' ''')
        months = self.cr.fetchall()
        FetchTables(months, self.tableWidget_25)

    def get_all_clients_from_db(self):
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, phone, groups, package, start_date, finish FROM daily_sales WHERE finish >= %s',(date.today().strftime('%Y-%m-%d'),))
        names = self.cr.fetchall()
        FetchTables(names, self.tableWidget_2)
    
    def search_all_clients(self):
        value = self.client_search.text()
        if value == "":
            self.get_all_clients_from_db()
        else:
            query = f'SELECT id, name, phone, groups, package, start_date, finish FROM daily_sales WHERE name LIKE %s or phone LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.get_all_clients_from_db()

            else:
                self.template_search(self.tableWidget_2, result)
    
    def get_all_coaches_from_db(self):
        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, phone, category FROM coach')
        names = self.cr.fetchall()
        FetchTables(names, self.tableWidget_10)
        self.get_category_item_from_database()

    def search_all_coach(self):
        value = self.coach_search.text()
        if value == "":
            self.get_all_coaches_from_db()
        else:
            query = f'SELECT id, name, phone, category FROM coach WHERE name LIKE %s or phone LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.get_all_coaches_from_db()

            else:
                self.template_search(self.tableWidget_10, result)

    def get_category_from_groups(self):
        self.category_table.setRowCount(0)
        self.category_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name FROM groups')
        names = self.cr.fetchall()
        FetchTables(names, self.category_table)
    
    def add_category_to_db(self):
        try:
            if self.lineEdit_3.text() =="":
                QMessageBox.about(self, "Warning", "please add category to add")
            else:
                self.cr.execute("INSERT INTO groups(name) VALUE(%s)",(self.lineEdit_3.text(),))
                self.db.commit()
                self.lineEdit_3.clear()
                self.get_category_from_groups()

        except Exception as e:
            print("add category", e)

    def show_all_costs(self):
        self.tabWidget_2.setCurrentIndex(2)
        self.get_costs_fromDB()
    
    def add_cost_to_db(self):
        try:
            if self.comboBox_3.currentIndex() == 0:
                QMessageBox.about(self, "Warning", "برجاء اختيار البيان من القائمة أعلاه")
            else:
                self.cr.execute(f'''INSERT INTO expense(name , price ,status, date )
                    VALUES('{self.comboBox_3.currentText()}','{self.lineEdit_10.text()}','{self.lineEdit_9.text()}','{date.today().strftime("%Y-%m-%d")}' )''')
                self.db.commit()
                QMessageBox.information(self, "success", "تم الإضافة بنجاح")
                self.lineEdit_9.clear()
                self.lineEdit_10.clear()
                self.comboBox_3.setCurrentIndex(0)
                self.get_costs_fromDB()

        except Exception as e :
            print(e)


    def get_costs_fromDB(self):
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_6.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.cr.execute('''SELECT name , price,status ,date FROM expense''')
        costs_data = self.cr.fetchall()
        self.tableWidget_6.setRowCount(0)
        FetchTables(costs_data, self.tableWidget_6)

    def show_clients_per_current_month(self):
        self.tableWidget_15.setRowCount(0)
        self.tableWidget_15.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name,groups FROM daily_sales WHERE finish >= %s',(date.today().strftime("%Y-%m-%d"),) )
        names = self.cr.fetchall()
        FetchTables(names, self.tableWidget_15)

    def search_show_clients_per_current_month(self):
        value = self.customer_lineEdit_2.text()
        if value == "":
            self.show_clients_per_current_month()
        else:
            query = f'SELECT id, name,groups FROM daily_sales WHERE finish >="{date.today().strftime("%Y-%m-%d")}" AND name LIKE %s or groups LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.show_clients_per_current_month()
            else:
                self.template_search(self.tableWidget_15, result)
    
    def handle_client_activity(self):
        row = self.tableWidget_15.currentItem().row()
        id = self.tableWidget_15.item(row, 0).text()
        self.cr.execute("SELECT name, groups FROM daily_sales WHERE id = %s",(id,))
        trainer = self.cr.fetchone()
        print(trainer)
        sessions.extend([[trainer[0],trainer[1], self.comboBox.currentText(),date.today().strftime("%Y-%m-%d"), str(datetime.now().strftime("%H:%M") )]])
        print(sessions)
        print('added successfully')
        self.session_table()
    
    def get_coach_to_comboBox(self):
        self.cr.execute("SELECT name FROM coach")
        all_coaches = self.cr.fetchall()
        for coach in all_coaches:
            self.comboBox.addItem(coach[0])
    
    def get_coaches(self):
        coaches.clear()
        self.cr.execute("SELECT name FROM coach")
        all_coaches = self.cr.fetchall()
        for coach in all_coaches:
            coaches.append(coach[0])

    def session_table(self):
        self.get_coaches()
        self.tableWidget_13.clear()
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.setColumnCount(4)
        self.tableWidget_13.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_13.setHorizontalHeaderLabels(['المتدرب', " الفئة", 'المدرب ', 'الحالة'])
        self.tableWidget_13.setRowCount(len(sessions))
        for row in range(len(sessions)):
            combo_box = QtWidgets.QComboBox()
            combo_box.clear()
            combo_box.addItems(coaches)
            combo_box.setCurrentText(str(sessions[row][2]))
            self.btn = QtWidgets.QPushButton('')
            icon_ = QtGui.QIcon()
            icon_.addPixmap(QtGui.QPixmap(":/yellow/icons/yellow/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.btn.setIcon(icon_)
            self.btn.setIconSize(QtCore.QSize(20, 20))
            self.btn.setStyleSheet("background-color: transparent;")
            self.tableWidget_13.setItem(row, 0, QTableWidgetItem(str((sessions[row][0]))))
            self.tableWidget_13.setItem(row, 1, QTableWidgetItem(str((sessions[row][1]))))
            self.tableWidget_13.setCellWidget(row, 2, combo_box)
            self.tableWidget_13.setCellWidget(row, 3, self.btn)

            self.btn.clicked.connect(self.delete_session_item)
            combo_box.currentIndexChanged.connect(self.edit_coach_in_table)
    
    def edit_coach_in_table(self):
        print(self.sender().currentText())
        row = self.tableWidget_13.indexAt(self.sender().pos()).row()
        sessions[row][2] = self.sender().currentText()
        self.session_table()

    def delete_session_item(self):
        row = self.tableWidget_13.indexAt(self.sender().pos()).row()
        print('delete item',row)
        sessions.pop(row)
        self.session_table()
        
    def add_new_session_invoice(self):
        self.cr.execute("INSERT INTO sessions(date) VALUE(%s)",( date.today().strftime(("%Y-%m-%d")),))
        self.db.commit()

    def add_to_temp_activity(self):
        try:
            
            if sessions == [] or self.tableWidget_12.rowCount() < 0:
                print('Nothing to add')
            else:
                self.add_new_session_invoice()
                self.cr.execute("SELECT id FROM sessions WHERE id=(SELECT max(id) FROM sessions); ")
                invoice = self.cr.fetchone()[0]

                for row in sessions:
                    self.cr.execute("INSERT INTO temp_activity(trainer, category, coach, date, start, invoice) VALUES(%s, %s,%s, %s, %s, %s)",
                    (row[0],row[1], row[2], row[3], str(row[4]), invoice))
                    self.db.commit()
                sessions.clear()
                self.session_table()


        except Exception as e:
            print(e)

    def finish_session(self):
        try:
            if sessions == [] or self.tableWidget_12.rowCount() < 0:
                print('Nothing to add')
            else:
                for row in sessions:
                    self.cr.execute("INSERT INTO activity(trainer, category, coach, date, start) VALUES(%s, %s,%s, %s, %s)",
                    (row[0],row[1], row[2], row[3], str(row[4])))
                    self.db.commit()
                sessions.clear()
                self.session_table()
                QMessageBox.about(self,"Done", "تمت انهاء الجلسة بنجاح")
        except Exception as e:
            QMessageBox.about(self, "Error", f"{e}")

    def from_temp_to_sessions(self):
        sessions.clear()
        row = self.tableWidget.currentItem().row()
        invoice = self.tableWidget.item(row, 0).text()
        self.cr.execute("SELECT * FROM temp_activity WHERE invoice = %s",(invoice,))
        sess = self.cr.fetchall()
        for s in sess:
            sessions.extend([[s[1],s[2],s[3], s[4], s[5]]])
        self.session_table()
        self.clients_activities_tab()
        self.cr.execute("Delete FROM temp_activity WHERE invoice = %s",(invoice,))
        self.db.commit()
        
    
    def show_existing_trainer(self):
        self.tableWidget_13.setRowCount(0)
        self.tableWidget_13.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name FROM groups')
        names = self.cr.fetchall()
        FetchTables(names, self.stocks_table)

    def hide_BTN(self):
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_5.tabBar().setVisible(False)
        self.tabWidget_9.tabBar().setVisible(False)
        self.tabWidget_7.tabBar().setVisible(False)
        self.tabWidget_2.tabBar().setVisible(False)
        self.frame_38.setVisible(False)
        self.label_15.setVisible(False)
        self.frame_45.setVisible(False)
        self.group_lbl.setVisible(False)
        self.groupBox_3.setVisible(False)
        self.pushButton_68.setVisible(False)
        self.pushButton_71.setVisible(False)      
        self.pushButton_74.setVisible(False)


    def main_window_(self):
        self.tabWidget.setCurrentIndex(32)
        self.categories_in_main_window()

    def groups_tab(self):
        self.tabWidget.setCurrentIndex(39)
        
        self.get_groups_from_db()

    def get_groups_from_db(self):
        self.stocks_table.setRowCount(0)
        self.stocks_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name FROM groups')
        names = self.cr.fetchall()
        FetchTables(names, self.stocks_table)

    def add_group_to_groups(self):
        self.cr.execute('INSERT INTO GROUPS(name) VALUE(%s)',(self.lineEdit_3.text(),))
        self.db.commit()
        self.lineEdit_3.clear()

        self.get_groups_from_db()
        # self.categories_in_main_window()
        # self.show_all_items()
    

# back sales invoice

    def add_client_to_db(self):
        try:
            if self.lineEdit_2.text() =="" or self.lineEdit_6.text() =="" :
                QMessageBox.about(self, "Warning", "Please add client name or phone")
            else:
                self.cr.execute(f"INSERT INTO clients(name, phone) VALUES('{self.lineEdit_2.text()}',{self.lineEdit_6.text()})")
                self.db.commit()
                self.lineEdit_2.clear()
                self.lineEdit_6.clear()
                self.frame_38.setVisible(False)
                self.get_clients_from_db()
        except Exception as e:
            print("add client error :- ", e)

    def get_clients_from_db(self):
        self.tableWidget_11.setRowCount(0)
        self.tableWidget_11.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT * FROM clients')
        names = self.cr.fetchall()
        self.tableWidget_11.setRowCount(len(names))
        for row in range(len(names)):
            self.btn = QtWidgets.QPushButton('تعديل')
            self.btn.setStyleSheet("background-color: transparent;")
            self.btn2 = QtWidgets.QPushButton('إضافة')
            self.btn2.setStyleSheet("background-color: transparent;")
            self.tableWidget_11.setItem(row, 0, QTableWidgetItem(str((names[row][0]))))
            self.tableWidget_11.setItem(row, 1, QTableWidgetItem(str((names[row][1]))))
            self.tableWidget_11.setItem(row, 2, QTableWidgetItem(str((names[row][2]))))
            self.tableWidget_11.setCellWidget(row, 3, self.btn)
            self.tableWidget_11.setCellWidget(row, 4, self.btn2)
            self.btn.clicked.connect(self.edit_clients)
            self.btn2.clicked.connect(self.select_client_to_invoice)        

    
    def edit_clients(self):
        row = self.tableWidget_11.indexAt(self.sender().pos()).row()
        id = self.tableWidget_11.item(row,0).text()
        print(id)
        name = self.tableWidget_11.item(row,1).text()
        phone = self.tableWidget_11.item(row,2).text()
        self.cr.execute("UPDATE clients SET name =%s, phone = %s WHERE id= %s ",(name, phone,id,))
        self.db.commit()
        self.get_clients_from_db()

    def select_client_to_invoice(self):
        row = self.tableWidget_11.indexAt(self.sender().pos()).row()
        self.lineEdit_36.setText(str(self.tableWidget_11.item(row, 1).text()))
        self.label_15.setText(str(self.tableWidget_11.item(row, 2).text()))
        self.tabWidget.setCurrentIndex(4)

    def search_sales_invoice(self):
        value = self.search_invoice_2.text()
        if value == "":
            self.show_invoice_to_edit()
        else:
            query = f'SELECT id, count, back, item_name, price, total, invoice FROM daily_sales WHERE count > 0 AND invoice LIKE %s or item_name LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.show_invoice_to_edit()

            else:
                for i in reversed(range(self.tableWidget_40.rowCount())):
                    self.tableWidget_40.removeRow(i)

                for row in range(len(result)):
                    self.tableWidget_40.insertRow(row)
                    self.btn_edit = QtWidgets.QPushButton('تعديل')
                    icon_ = QtGui.QIcon()
                    icon_.addPixmap(QtGui.QPixmap(":/yellow/icons/yellow/edit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.btn_edit.setIcon(icon_)
                    self.btn_edit.setIconSize(QtCore.QSize(25, 25))
                    
                    self.tableWidget_40.setItem(row, 0, QTableWidgetItem(str(result[row][0])))
                    self.tableWidget_40.setItem(row, 1, QTableWidgetItem(str(result[row][1])))
                    self.tableWidget_40.setItem(row, 2, QTableWidgetItem(str('0')))
                    self.tableWidget_40.setItem(row, 3, QTableWidgetItem(str(result[row][3])))
                    self.tableWidget_40.setItem(row, 4, QTableWidgetItem(str(result[row][4])))
                    self.tableWidget_40.setItem(row, 5, QTableWidgetItem(str(result[row][5])))
                    self.tableWidget_40.setItem(row, 6, QTableWidgetItem(str(result[row][6])))
                    self.tableWidget_40.setCellWidget(row, 7, self.btn_edit)

                    self.btn_edit.clicked.connect(self.handle_edit_btn)

#end back sales invoice
    def little_sales_tab(self):
        self.tabWidget.setCurrentIndex(22)
        self.showlittle_Sales()

# start suppliers accounts show , export and filter
    def go_to_suppliers_accounts(self):
        self.tabWidget.setCurrentIndex(43)
        self.supplier_accounts_widget_recipts()
        self.handle_search_suppliers_accounts()

    def go_to_suppliers_accounts_widget(self):
        self.tableWidget_38.setRowCount(0)
        self.tableWidget_38.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        self.cr.execute('SELECT id,name, invoice,total, paid, remain, pay_date  FROM recipt_pay')
        items = self.cr.fetchall()
        sorted_list = sorted(items, key=lambda item: item[2])
        FetchTables(sorted_list, self.tableWidget_38)
    
    def supplier_accounts_widget_recipts(self):
        self.tableWidget_38.setRowCount(0)
        self.tableWidget_38.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        self.cr.execute('SELECT id,name, invoice,total, paid, remain, invoice_date  FROM recipts')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_38)

    def supplier_accounts_widget_recipts_by_dates(self):
        self.tableWidget_38.setRowCount(0)
        self.tableWidget_38.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        self.cr.execute('SELECT id,name, invoice,total, paid, remain, invoice_date  FROM recipts WHERE invoice_date BETWEEN %s AND %s',
            (self.dateEdit_6.date().toPyDate(),self.dateEdit_7.date().toPyDate(),))
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_38)
    
    def go_to_suppliers_accounts_widget_by_dates(self):
        self.tableWidget_38.setRowCount(0)
        self.tableWidget_38.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)

        self.cr.execute('SELECT id,name, invoice,total, paid, remain, pay_date  FROM recipt_pay WHERE pay_date BETWEEN %s AND %s',
            (self.dateEdit_6.date().toPyDate(),self.dateEdit_7.date().toPyDate(),))
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_38)

    def handle_export_suppliers(self):
        if self.comboBox_10.currentIndex() == 0:
            self.export_supplier_accounts_report()
        elif self.comboBox_10.currentIndex() == 1:
            self.export_supplier_accounts_report_recipts()

    def export_supplier_accounts_report(self):
        try:
            self.cr.execute('SELECT id,name, invoice,total, paid, remain, pay_date  FROM recipt_pay WHERE name = %s AND pay_date BETWEEN %s AND %s',
                (self.label_33.text(), self.dateEdit_10.date().toPyDate(),self.dateEdit_11.date().toPyDate(),))
            items = self.cr.fetchall()

            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            cells = file.add_format()
            cells.set_font_size(13)
            cells.set_bold()
            cells.set_align('center')
            cells.set_border()

            merge_format = file.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size':14})
            date_time = datetime.strptime(str(date.today()),'%Y-%m-%d')
            date_format = file.add_format({'num_format': "d mmmm yyy",
                                    'align': 'center',
                                    'font_size':14,
                                    })
            
            sheet = file.add_worksheet()
            sheet.write_datetime(0,1, date_time, date_format)
            sheet.set_column('B:B', 30)
            sheet.set_column('G:G', 13)
            sheet.write(3,5,"مـن",cells)
            sheet.write(3,2,"إلى" ,cells)

            sheet.merge_range('D1:F1','بيان تفصيلى مدفوعات للتاجر', cells)
            sheet.merge_range('B2:F3',f' اسم التاجر/المورد : {self.label_33.text()}', merge_format)

            sheet.write(3,1,f"{self.dateEdit_10.date().toPyDate()}", cells)

            sheet.merge_range('D4:E4',f'{self.dateEdit_11.date().toPyDate()}', cells)
            
            sheet.write(4, 0,"مسلسل", cells)
            sheet.write(4, 1,"الاسم", cells)
            sheet.write(4, 2,"الفاتورة", cells)
            sheet.write(4, 3,"الإجمالى",cells)
            sheet.write(4, 4,"المدفوع",cells)
            sheet.write(4, 5,"المتبقى",cells)
            sheet.write(4, 6,"تاريخ السداد",cells)

            row_number = 5
            for row in items:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item),cells)
                    column_number += 1
                row_number += 1
            file.close()
        except Exception as e:
            print(e)

    def export_supplier_accounts_report_recipts(self):
        try:
            self.cr.execute('SELECT id,name, invoice,total, paid, remain, invoice_date  FROM recipts WHERE name = %s AND invoice_date BETWEEN %s AND %s',
                (self.label_33.text(), self.dateEdit_10.date().toPyDate(),self.dateEdit_11.date().toPyDate(),))
            items = self.cr.fetchall()

            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            cells = file.add_format()
            cells.set_font_size(13)
            cells.set_bold()
            cells.set_align('center')
            cells.set_border()

            merge_format = file.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
                'font_size':14})
            date_time = datetime.strptime(str(date.today()),'%Y-%m-%d')
            date_format = file.add_format({'num_format': "d mmmm yyy",
                                    'align': 'center',
                                    'font_size':14,
                                    })
            
            sheet = file.add_worksheet()
            sheet.write_datetime(0,1, date_time, date_format)
            sheet.set_column('B:B', 30)
            sheet.set_column('G:G', 13)
            sheet.write(3,5,"مـن",cells)
            sheet.write(3,2,"إلى" ,cells)

            sheet.merge_range('D1:F1','بيان  لفواتير التاجر/ المورد', cells)
            sheet.merge_range('B2:F3',f' اسم التاجر/المورد : {self.label_33.text()}', merge_format)

            sheet.write(3,1,f"{self.dateEdit_10.date().toPyDate()}", cells)

            sheet.merge_range('D4:E4',f'{self.dateEdit_11.date().toPyDate()}', cells)
            
            sheet.write(4, 0,"مسلسل", cells)
            sheet.write(4, 1,"الاسم", cells)
            sheet.write(4, 2,"الفاتورة", cells)
            sheet.write(4, 3,"الإجمالى",cells)
            sheet.write(4, 4,"المدفوع",cells)
            sheet.write(4, 5,"المتبقى",cells)
            sheet.write(4, 6,"تاريخ الفاتورة",cells)

            row_number = 5
            for row in items:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item),cells)
                    column_number += 1
                row_number += 1
            file.close()
        except Exception as e:
            print(e)

    def handle_search_suppliers_accounts(self):
        if self.comboBox_6.currentIndex() == 1:

            if self.checkBox_2.isChecked():
                self.go_to_suppliers_accounts_widget_by_dates()
            else: 
                self.go_to_suppliers_accounts_widget()

        elif self.comboBox_6.currentIndex() == 0:
            if self.checkBox_2.isChecked():
                self.supplier_accounts_widget_recipts_by_dates()
            else:
                self.supplier_accounts_widget_recipts()

    def search_supplier_recipts(self):
        value = self.search_account.text()
        if value == "":
            self.supplier_accounts_widget_recipts()
        else:
            query = f'SELECT id,name, invoice,total, paid, remain, invoice_date  FROM recipts WHERE id LIKE %s or name LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.supplier_accounts_widget_recipts()

            else:
                self.template_search(self.tableWidget_38, result)

    def show_report_accounts(self):
        self.dateEdit_10.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit_11.setDateTime(QtCore.QDateTime.currentDateTime())
        row = self.tableWidget_38.currentItem().row()
        supplier = self.tableWidget_38.item(row,1).text()
        self.label_33.setText(str(supplier))
        self.frame_18.setVisible(True)
    
    def hide_frame_7(self):
        self.frame_18.setVisible(False)

    def suppliery_summary_report_recipt_pays(self):
        f = open("account.html", 'w', encoding="utf-8")

        html =f''' 
            <!DOCTYPE html>
            <html lang="ar">
                <head >
                    <meta charset="utf-8">
                    <link rel="stylesheet" href="style.css">

                </head>
                <body >
                
                <div style="overflow: hidden;">
                    <p class="lef" style="float: left;">{date.today().strftime('%Y:%m:%d')}</p>
                    <p class="p-2 righ" style="float: right;">بيان تفصيلى لتعاملات التاجر </p>
                </div>
                <h1  class='centered'>حساب  {self.label_33.text()}</h1>
                <div class ="centered" style="font-size:12px";>
                    <p> من {self.dateEdit_10.date().toPyDate()}</p>
                    <p>الى {self.dateEdit_11.date().toPyDate()}</p>
                </div>
                <table id="customers">
                        <tr >
                            <th>الفاتورة</th>
                            <th>الاجمالى</th>
                            <th>المدفوع</th>
                            <th>المتبقى</th>
                            <th> تاريخ السداد</th>
                        </tr> 
        '''
        self.cr.execute('SELECT invoice, total, paid, remain, pay_date FROM recipt_pay WHERE name = %s AND pay_date BETWEEN %s AND %s',
                (self.label_33.text(), self.dateEdit_10.date().toPyDate(),self.dateEdit_11.date().toPyDate(),))
        items = self.cr.fetchall()

        for item in items:
            html = html + f''' <tr style="text-align:center">
                                        <td>{item[0]}</td>
                                        <td>{item[1]}</td>
                                        <td>{item[2]}</td>
                                        <td>{item[3]}</td>
                                        <td>{item[4]}</td>
                                    </tr>
                                '''

        html = html + """
            </table>
            <p class ="centered">شكرا لزيارتكم</p>
        """ 
        f.write(html)
        f.close()
        self.view_account_recipt()

    def suppliery_summary_report_recipts(self):
        f = open("account.html", 'w', encoding="utf-8")

        html =f''' 
            <!DOCTYPE html>
            <html lang="ar">
                <head >
                    <meta charset="utf-8">
                    <link rel="stylesheet" href="style.css">

                </head>
                <body >
                
                <div style="overflow: hidden;">
                    <p class="lef" style="float: left;">{date.today().strftime('%Y:%m:%d')}</p>
                    <p class="p-2 righ" style="float: right;">بيان فواتير التاجر</p>
                </div>
                <h1  class='centered'>حساب  {self.label_33.text()}</h1>
                <div class ="centered" style="font-size:12px";>
                    <p> من {self.dateEdit_10.date().toPyDate()}</p>
                    <p>الى {self.dateEdit_11.date().toPyDate()}</p>
                </div>
                <table id="customers">
                        <tr >
                            <th>الفاتورة</th>
                            <th>الاجمالى</th>
                            <th>المدفوع</th>
                            <th>المتبقى</th>
                            <th> تاريخ الفاتورة</th>
                        </tr> 
        '''
        self.cr.execute('SELECT invoice, total, paid, remain, invoice_date FROM recipts WHERE name = %s AND invoice_date BETWEEN %s AND %s',
                (self.label_33.text(), self.dateEdit_10.date().toPyDate(),self.dateEdit_11.date().toPyDate(),))
        items = self.cr.fetchall()

        for item in items:
            html = html + f''' <tr style="text-align:center">
                                        <td>{item[0]}</td>
                                        <td>{item[1]}</td>
                                        <td>{item[2]}</td>
                                        <td>{item[3]}</td>
                                        <td>{item[4]}</td>
                                    </tr>
                                '''

        html = html + """
            </table>
            <p class ="centered">شكرا لزيارتكم</p>
        """ 
        f.write(html)
        f.close()
        self.view_account_recipt()

    def handle_report_printing(self):
        if self.comboBox_10.currentIndex() == 0:
            self.suppliery_summary_report_recipt_pays()
        elif self.comboBox_10.currentIndex() == 1:
            self.suppliery_summary_report_recipts()

    def view_account_recipt(self):
        self.webEngineView_2 = QWebEngineView()
        self.vbox_2.addWidget(self.webEngineView_2)
        self.webEngineView_2.load(QtCore.QUrl.fromLocalFile(
            os.path.abspath(os.path.dirname(__file__)) + "/" + f"account.html"))
        
        self.webEngineView_2.loadFinished.connect(self.print_account_recipt)

        # self.tabWidget.setCurrentIndex(45)
        self.clearCache(self.webEngineView_2)

    def print_account_recipt(self):
        self._printer = QtPrintSupport.QPrinter()
        QPrinter.setResolution(self._printer, 800)
        self.webEngineView_2.page().print(self._printer, self.printResult)

# End suppliers accounts show , export and filter

    def go_to_suspession_recipts(self):
        self.tabWidget.setCurrentIndex(42)
        self.show_suspession_recipts()

    def show_suspession_recipts(self):
        try:
            self.tableWidget_37.setRowCount(0)
            self.tableWidget_37.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.cr.execute('SELECT id, customer, item_id, price, total, suspession_recipt FROM suspesion ')
            items = self.cr.fetchall()
            FetchTables(items, self.tableWidget_37)
        except Exception as e:
            QMessageBox.warning(self,"error", str(e))

    def go_to_count_stocks(self):
        self.tabWidget.setCurrentIndex(41)
        self.count_stocks()
    
    def count_stocks(self):
        self.tableWidget_74.setRowCount(0)
        self.tableWidget_74.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, name, price, groups FROM item')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_74)
        self.get_stock_items_()
    

    def to_today_purchase(self):
        self.tabWidget.setCurrentIndex(40)
        self.tabWidget_8.setCurrentIndex(0)
        self.today_purchase()
    
    def today_purchase(self):
        self.tableWidget_72.setRowCount(0)
        self.tableWidget_72.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT recipt, item, item_price, count, total, date FROM purchase_recipt WHERE date =%s ',
        (date.today().strftime("%Y:%m:%d"),))
        item = self.cr.fetchall()
        FetchTables(item, self.tableWidget_72)

    def to_toady_backs(self):
        self.tabWidget.setCurrentIndex(40)
        self.tabWidget_8.setCurrentIndex(1)
        self.today_backs()
    
    def today_backs(self):
        self.tableWidget_73.setRowCount(0)
        self.tableWidget_73.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute(f'SELECT recipt, item, count, price, recipt_date FROM back_items WHERE recipt_date ="{date.today().strftime("%Y:%m:%d")}" ')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_73)

    def go_to_item_summary(self):
        self.tabWidget.setCurrentIndex(38)

    def show_summary_item_sales(self):
        self.tableWidget_36.clear()
        self.tableWidget_36.setRowCount(0)
        self.tableWidget_36.setColumnCount(6)
        self.tableWidget_36.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_36.setHorizontalHeaderLabels(['مسلسل','الصنف',"العدد",'السعر','الاجمالى','التاريخ'])
        self.cr.execute('SELECT id, item_name, count, price, total, date FROM daily_sales WHERE item_name = %s ',(self.lineEdit_85.text(),))
        item = self.cr.fetchall()
        FetchTables(item, self.tableWidget_36)
        self.count_item_sales_purchase_backs()

    def show_summary_item_purchases(self):
        self.tableWidget_36.clear()
        self.tableWidget_36.setRowCount(0)
        self.tableWidget_36.setColumnCount(6)
        self.tableWidget_36.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_36.setHorizontalHeaderLabels(['فاتورة','الصنف',"سعر الوحدة",'العدد','اجمالى السعر','التاريخ'])
        self.cr.execute('SELECT recipt, item, item_price, count, total, date FROM purchase_recipt WHERE item =%s ',(self.lineEdit_85.text(),))
        item = self.cr.fetchall()
        FetchTables(item, self.tableWidget_36)
        self.count_item_sales_purchase_backs()

    def show_summary_item_backs(self):
        self.tableWidget_36.clear()
        self.tableWidget_36.setRowCount(0)
        self.tableWidget_36.setColumnCount(6)
        self.tableWidget_36.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_36.setHorizontalHeaderLabels(['مسلسل','الصنف','العدد','السعر','التاريخ',"فاتورة"])  
        self.cr.execute('SELECT id, item, count, price, recipt_date, recipt FROM back_items WHERE item =%s ',(self.lineEdit_85.text(),))
        item = self.cr.fetchall()
        FetchTables(item, self.tableWidget_36)
        self.count_item_sales_purchase_backs()

    def count_item_sales_purchase_backs(self):
        try:
            self.cr.execute('SELECT COUNT(id) FROM daily_sales WHERE item_name = %s ',(self.lineEdit_85.text(),))
            count_sales = self.cr.fetchone()[0]
            self.label_440.setText(str(count_sales))

            self.cr.execute('SELECT COUNT(id) FROM purchase_recipt WHERE item = %s ',(self.lineEdit_85.text(),))
            count_purchase = self.cr.fetchone()[0]
            self.label_441.setText(str(count_purchase))

            self.cr.execute('SELECT COUNT(id) FROM back_items WHERE item = %s ',(self.lineEdit_85.text(),))
            count_backs = self.cr.fetchone()[0]
            self.label_442.setText(str(count_backs))
        except:
            pass


    def show_add_paid_to_invoice_frame(self):
        self.frame_52.setVisible(True)

    def hide_paid_to_invoice_frame(self):
        self.frame_52.setVisible(False)

    def return_paids_to_invoice(self):
        self.cr.execute(f'''UPDATE recipts SET paid= paid - "{Decimal(self.lineEdit_87.text())}" ,
            remain =remain + "{Decimal(self.lineEdit_87.text())}" WHERE invoice = '{self.label_124.text()}' ''')
        self.db.commit()
        self.frame_52.setVisible(False)
        self.lineEdit_87.clear()
        self.summaryDbtTab()


    def expand_collapse(self):
        """
        toggle right sidebar
        """
        if self.label_153.text() == '1':
            self.frame_11.setVisible(False)
            self.label_153.setText('0')

        else:
            self.frame_11.setVisible(True)
            self.label_153.setText('1')

    def businessInfo(self):
        self.setWindowIcon(QIcon('awg.ico'))
        try:
            self.cr.execute('select * from info')
            info = self.cr.fetchone()
            info_1 = info[1]

            self.setWindowTitle(f'{info_1} ')
        except:
            self.setWindowTitle(str('Awg Solutions'))

    def show_recipt_tab(self):
        self.tabWidget.setCurrentIndex(35)
        invoice = self.label_124.text()
        self.label_60.setText(str(invoice))
        self.widget_12.load(QtCore.QUrl.fromLocalFile(
            os.path.abspath(os.path.dirname(__file__)) + "/" + f"invoices\\recipts\\{invoice}.html"))

    def print_recipt(self):
        self._printer = QtPrintSupport.QPrinter()
        QPrinter.setResolution(self._printer, 800)
        self.widget_12.page().print(self._printer, self.printResult)


    def show_add_small_frame(self):
        self.frame_45.setVisible(True)

    def hide_add_small_frame(self):
        self.frame_45.setVisible(False)

    def show_add_big_frame(self):
        self.frame_46.setVisible(True)

    def hide_add_big_frame(self):
        self.frame_46.setVisible(False)

    def show_hidden_frame(self):
        self.frame_44.setVisible(True)

    def show_hidden_frame2(self):
        self.frame_49.setVisible(True)

    def hide_add_supplier_back_recipt(self):
        self.frame_49.setVisible(False)

    def add_supplier_to_database(self):
        if self.lineEdit_31.text() == "" or self.lineEdit_34.text() == "":
            QMessageBox.warning(self, "تنبية", "لابد من استكمال البيانات ")
        if len(self.lineEdit_34.text()) != 11:
            QMessageBox.warning(self, 'warning', "تأكد من صحة رقم الهاتف .. لقد أدخلت رقم خاطئ")
        else:
            try:
                self.cr.execute('SELECT name FROM b2b_accounts where name = %s ', (self.lineEdit_31.text(),))
                name = self.cr.fetchone()[0]
                print(name)
                if name:
                    QMessageBox.warning(self, 'تنبية', 'التاجر موجود بالفعل لديك')
            except TypeError:
                self.cr.execute(
                    '''Insert INTO b2b_accounts(name, phone, total, paid, remain) VALUES(%s, %s, %s, %s, %s) ''',
                    (self.lineEdit_31.text(), self.lineEdit_34.text(), 0, 0, 0))
                self.db.commit()
                self.show_suppliers()
                self.comboBox_8.setCurrentText(str(self.lineEdit_31.text()))
                QMessageBox.about(self, " تم بنجاح", "تمت الاضافة بنجاح")
                self.frame_44.setVisible(False)
                self.lineEdit_31.clear()
                self.lineEdit_34.clear()
                
            except Exception as e:
                QMessageBox.about(self, 'Error', str(e))

    def add_supplier_to_database2(self):
        if self.lineEdit_77.text() == "" or self.lineEdit_78.text() == "":
            QMessageBox.warning(self, "تنبية", "لابد من استكمال البيانات ")

        if len(self.lineEdit_78.text()) != 11:
            QMessageBox.warning(self, 'warning', "تأكد من صحة رقم الهاتف .. لقد أدخلت رقم خاطئ")
        else:
            try:
                self.cr.execute('SELECT name FROM b2b_accounts where name = %s ', (self.lineEdit_77.text(),))
                name = self.cr.fetchone()[0]
                print(name)
                if name:
                    QMessageBox.warning(self, 'تنبية', 'التاجر موجود بالفعل لديك')

            except TypeError:
                self.cr.execute(
                    '''Insert INTO b2b_accounts(name, phone, total, paid, remain) VALUES(%s, %s, %s, %s, %s) ''',
                    (self.lineEdit_77.text(), self.lineEdit_78.text(), 0, 0, 0))
                self.db.commit()
                self.show_suppliers_to_back_purchase()
                QMessageBox.about(self, " تم بنجاح", "تمت الاضافة بنجاح")
                self.frame_49.setVisible(False)

            except Exception as e:
                QMessageBox.about(self, 'Error', str(e))

    def close_supplier_window(self):
        self.frame_44.setVisible(False)

    def add_purchase_invoice_tab(self):
        self.tabWidget.setCurrentIndex(34)
        self.show_suppliers()
        self.generate_recipt()


    def add_recipt_tab(self):
        self.tabWidget.setCurrentIndex(37)
        self.show_suppliers_to_back_purchase()
        self.generate_back_recipt()

    def customer_order_tab(self):
        self.tabWidget.setCurrentIndex(26)
        self.show_customer_order()
    
    def handle_combo_cusomer(self):
        if self.comboBox_5.currentIndex() ==0:
            self.show_customer_order()
        else:
            self.show_customer_order_today()

    def show_customer_order(self):
        self.customer_search_lineEdit.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 50)
        self.tableWidget.setColumnWidth(4, 50)
        self.tableWidget.setColumnWidth(5, 70)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT invoice,name, phone, total, discount, invoice_date FROM invs ')
        sales = self.cr.fetchall()
        FetchTables(sales, self.tableWidget)

    def show_customer_order_today(self):
        self.customer_search_lineEdit.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 120)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 50)
        self.tableWidget.setColumnWidth(4, 50)
        self.tableWidget.setColumnWidth(5, 70)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute(f'SELECT invoice,name, phone, total, discount, invoice_date FROM invs WHERE invoice_date ="{date.today()}" ')
        sales = self.cr.fetchall()
        FetchTables(sales, self.tableWidget)

    def search_customer_order(self):
        value = self.customer_search_lineEdit.text()
        if value == "":
            print('nothing to search')
            self.show_customer_order()
        else:
            query = f'SELECT invoice,name, phone, total, discount, invoice_date FROM invs WHERE name LIKE %s or phone LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                print("nothing to search")
                self.show_customer_order()

            else:
                self.template_search(self.tableWidget, result)

    def show_all_sales_(self):
        self.cr.execute("SELECT name, phone, groups, package, price, start_date, finish, invoice FROM daily_sales ")
        self.tableWidget_14.setRowCount(0)
        self.tableWidget_14.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        FetchTables(self.cr.fetchall(), self.tableWidget_14)
        self.tabWidget.setCurrentIndex(18)

    def search_show_all_sales_(self):
        value = self.sales_search.text()
        if value == "":
            print('nothing to search')
            self.show_all_sales_()
        else:
            query = f'SELECT name, phone, groups, package, price, start_date, finish, invoice FROM daily_sales WHERE name LIKE %s or phone LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                print("nothing to search")
                self.show_all_sales_()

            else:
                self.template_search(self.tableWidget_14, result)

    def get_daily_sales_by_gender(self):
        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('SELECT id, customer, item_name, count, price, total, discount, date, invoice FROM daily_sales WHERE gender LIKE %s ',(self.comboBox_2.currentText(),))
        sales = self.cr.fetchall()
        FetchTables(sales, self.tableWidget_3)

    def get_category_item_from_database(self):
        self.comboBox_2.clear()
        self.comboBox_2.addItem("اختر الفئة المخصصة")
        self.cr.execute('SELECT name FROM groups ')
        stock_items = self.cr.fetchall()
        for stock in stock_items:
            self.comboBox_2.addItem(stock[0])

    def add_email_tab(self):
        self.tabWidget.setCurrentIndex(6)
        try:
            self.cr.execute('SELECT mail FROM info')
            alert = self.cr.fetchone()[0]
            self.lineEdit_61.setText(str(alert))

        except Exception as e:
            print(e)

    def update_mail(self):
        try:
            if not self.lineEdit_61.text().endswith('@gmail.com'):
                QMessageBox.about(self, "Error", "تأكد من أن البريد المدخل هو gmail.com")
            else:
                self.cr.execute('UPDATE info SET mail = %s', (self.lineEdit_61.text(),))
                self.db.commit()
                self.add_category()
        except Exception as EX:
            print(str(EX))

    def editInfo(self):
        self.tabWidget.setCurrentIndex(18)
        self.cr.execute(f'SELECT * FROM INFO')
        info = self.cr.fetchone()
        self.label_130.setText(str(info[1]))
        self.lineEdit_46.setText(str(info[2]))
        self.lineEdit_45.setText(str(info[4]))

    def editInfoConfirm(self):
        query = ' UPDATE info SET address = %s , addition = %s  ,qr = %s'
        value = ( self.lineEdit_46.text(), self.lineEdit_45.text(),self.textEdit.toPlainText())
        self.cr.execute(query, value)
        self.db.commit()
        self.generate_qr_for_receipt()
        self.add_category()

    def template_search(self, table, result):
        self.table = table
        self.result = result
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)

        for rowData in self.result:
            rowNumber = self.table.rowCount()
            self.table.insertRow(rowNumber)
            for col, item_data in enumerate(rowData):
                self.table.setItem(rowNumber, col, QTableWidgetItem(str(item_data)))

    def sales_widget_table(self):  # test1 before
        try:
            print("data in sales widget table", data)
            self.tableWidget_12.clear()
            self.tableWidget_12.setColumnCount(5)
            self.tableWidget_12.setColumnWidth(2, 42)
            self.tableWidget_12.setColumnWidth(3, 42)
            
            self.tableWidget_12.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            self.tableWidget_12.setHorizontalHeaderLabels(["فئة","باقة","عدد","سعر","انتهاء"])
            self.tableWidget_12.setRowCount(len(data))
            self.sum_cart()
            for row in range(len(data)):
                
                self.tableWidget_12.setItem(row, 0, QTableWidgetItem(str((data[row][0]))))
                self.tableWidget_12.setItem(row, 1, QTableWidgetItem(str((data[row][1]))))
                self.tableWidget_12.setItem(row, 2, QTableWidgetItem(str((data[row][2]))))
                self.tableWidget_12.setItem(row, 3, QTableWidgetItem(str((data[row][3]))))
                self.tableWidget_12.setItem(row, 4, QTableWidgetItem(str((data[row][5]))))
                
        except Exception as e:
            print(e)


    def sum_cart(self):
        itemsSum = 0
        for row in data:
            itemTotal = int(row[3])
            itemsSum = itemTotal + itemsSum
        self.itemsSum = itemsSum
        self.tableWidget_12.clearSelection()
        self.label_2.setText(str(self.itemsSum))

    def addem(self):
        
        try: 
            self.cr.execute(f"SELECT * FROM items WHERE name = '{self.sender().text()}' and groups = '{self.group_lbl.text()}'  ")
            item = self.cr.fetchone()
            print("the item is => ", item)

            today = date.today().strftime("%Y:%m:%d")
            input_dt =datetime(int(today[:4]), int(today[5:7]), int(today[8:]))
            next_month = input_dt.replace(day=28) + timedelta(days=4)
            end_month = next_month - timedelta(days=next_month.day)

            data.extend([[item[4], item[1], item[2], item[3] ,date.today().strftime("%Y:%m:%d"), end_month.date()]])
            print(data)
            self.sales_widget_table()

        except Exception as e:
            print('error', e)

    def deleteItem(self):
        index = (self.tableWidget_12.selectionModel().currentIndex())
        print(index)
        if index.row() != -1:
            data.pop(index.row())
            self.sales_widget_table()
            self.tableWidget_12.clearSelection()

        self.sales_widget_table()

    def editcells(self):
        try:
            edited_row = self.tableWidget_12.currentItem().row()
            headercount = self.tableWidget_12.columnCount()
            for index, value in enumerate(data):
                for x in range(headercount):
                    count = self.tableWidget_12.item(edited_row,2).text()  # get cell text at row, col
                    price = self.tableWidget_12.item(edited_row,3).text()
                    finish_date = self.tableWidget_12.item(edited_row,4).text()
                    if index == edited_row:
                        try:
                            if int(count) <= 0 or int(price) <= 0:
                                QMessageBox.about(self, "Warning", "رجاء ادخال رثم أكبر من الصفر")
                                self.sales_widget_table()
                            else:
                                data[index][3] = int(price)
                                data[index][2] = int(count)
                                data[index][5] = str(finish_date)
                        except ValueError:
                            QMessageBox.about(self, "Warning", "لقد أدخلت أحرف بدلا من الأرقام")
                            self.sales_widget_table()
            self.sum_cart()
          
        except Exception as e:
            print(e)

    def validate_finish_date(self):
        try:
             for row in data:
                print(row[5])         
                datetime.strptime(str(row[5]), '%Y-%m-%d')
                self.insertIntoDb()
                print("==> Correct date string")
        except ValueError:
            print(data)
            print("==> Not Correct date string")
            QMessageBox.about(self, " التاريخ","الرجاء ادخال التاريخ بطريقة صحيحة")
        except Exception as e:
            print("==> Not Correct date string 2", e)
            QMessageBox.about(self, " التاريخ","الرجاء ادخال التاريخ بطريقة صحيحة")

    def insertIntoDb(self):
        self.add_new_invoice_number()
        self.cr.execute(f'''SELECT invoice FROM invs WHERE id=(SELECT max(id) FROM invs);''')
        invoice = self.cr.fetchone()[0]
        print(invoice)
        for row in data:
            if data == [] or self.tableWidget_12.rowCount() < 0:
                print('Nothing to add')
            else:
                try:
                    if self.lineEdit_36.text() == "":
                        QMessageBox.about(self, "Warning", "برجاء ادخال اسم العميل")
                    else:
                        self.cr.execute(f''' INSERT INTO daily_sales (name, phone,groups, package, count, price, start_date, finish, invoice)
                            VALUES("{self.lineEdit_36.text()}", "{self.label_15.text()}" ,"{row[0]}", "{row[1]}", "{row[2]}", "{row[3]}",
                            "{date.today().strftime('%Y-%m-%d')}", "{row[5]}" , "{invoice}") ''')
                        self.db.commit()
                except Exception as e:
                    print("add new invoice ", e)

        print('daily sales is done')
        self.printIt()
        self.group_()

    
    def search_customer_to_add_to_account(self):
        value = self.customer_lineEdit.text()
        if value == "":
            self.get_clients_from_db()
        else:
            query = f'SELECT * FROM clients WHERE name LIKE %s or phone LIKE %s '
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            print(result)
            if not result:
                self.get_clients_from_db()

            else:
                for i in reversed(range(self.tableWidget_11.rowCount())):
                    self.tableWidget_11.removeRow(i)

                for row in range(len(result)):
                    self.tableWidget_11.insertRow(row)
                    self.btn = QtWidgets.QPushButton('تعديل')
                    self.btn.setStyleSheet("background-color: transparent;")
                    self.btn2 = QtWidgets.QPushButton('إضافة')
                    self.btn2.setStyleSheet("background-color: transparent;")
                    self.tableWidget_11.setItem(row, 0, QTableWidgetItem(str((result[row][0]))))
                    self.tableWidget_11.setItem(row, 1, QTableWidgetItem(str((result[row][1]))))
                    self.tableWidget_11.setItem(row, 2, QTableWidgetItem(str((result[row][2]))))
                    self.tableWidget_11.setCellWidget(row, 3, self.btn)
                    self.tableWidget_11.setCellWidget(row, 4, self.btn2)
                    self.btn.clicked.connect(self.edit_clients)
                    self.btn2.clicked.connect(self.select_client_to_invoice)   
                

    def group_(self):
        self.cleanorder()
        data.clear()

    def add_new_invoice_number(self):
        try:
            self.cr.execute('SELECT invoice FROM invs WHERE id=(SELECT max(id) FROM invs);')
            invoice = self.cr.fetchone()[0]
            new_invoice = invoice[:4] + str(int(invoice[4:]) + 1).zfill(5)
            if self.lineEdit_36.text() == "":
               print("name isn\'t exist")
            else:
                self.cr.execute(f''' INSERT INTO invs(invoice, date) Values("{new_invoice}", '{date.today().strftime("%Y:%m:%d")}' ) ''')
                self.db.commit()
                print('invoice has been inserted')
        except TypeError:
            self.cr.execute(f'''INSERT INTO invs (invoice,date) Values("INV-0000",'{date.today().strftime("%Y:%m:%d")}') ''')
            self.db.commit()
            self.add_new_invoice_number()
        except Exception as ex:
            print("add invoice error",ex)


    def printIt(self):
        self.cr.execute(f'''SELECT invoice FROM invs WHERE id=(SELECT max(id) FROM invs);''')
        invoice = self.cr.fetchone()[0]

        self.cr.execute('SELECT * FROM info')
        info = self.cr.fetchone()
        def_date = datetime.now()
        date_ = def_date.strftime("%Y-%m-%d")

        f = open("Screen\\invoice.html", 'w', encoding="utf-8")
        f2 = open(f"invoices\\invoices\\{invoice}.html", 'w', encoding="utf-8")
        message = f"""
            <!DOCTYPE html>
            <html lang="ar">
                <head >
                    <meta charset="utf-8">
                    <link rel="stylesheet" href="style.css">

                </head>
                <body >
                <h1  class='centered'>{info[1]}</h1>
                <p class="centered" style="font-size: 16px;";>{info[2]}<p/>

                <div style="overflow: hidden;">
                    <p class="lef" style="float: left;">{invoice}</p>
                    <p class="p-2 righ" style="float: right;">{date_}</p>
                </div> 
                <p class="centered" style="font-size: 16px;";>اسم المشترك:- {self.lineEdit_36.text()}<p/>
                
                """
        message = message + """<table>
                        <tr >
                            <th>تمرين</th>
                            <th>باقة</th>
                            <th>سعر </th>
                            <th>تاريخ الانتهاء</th>
                        </tr> """

        for row in data:
          
            message = message + f'''   
                                    <tr style="text-align:center">
                                        <td>{row[0]}</td>
                                        <td>{row[1]}</td>
                                        <td>{row[3]}</td>
                                        <td>{row[5]}</td>
                                    </tr>
                                    '''
           

        end = (f'''</table>
            <footer dir="rtl">
                <div style="width:99.5%;border: 1px solid black;border-collapse: collapse;
                display: flex;justify-content: space-between;text-align: center;align-content: center;">
                    <p>إجمالى المستحق :{self.label_2.text()}</p>
                </div>
                
                <div>
                    <p class='centered' >{info[4]}</p>
                    <p class='centered'> {info[5]}</p>
                </div>

                </footer>
                </div>
            </body>
            ''')
        f.write(message + end)
        f.close()
        f2.write(message + end)
        f2.close()
        self.printingReciptIf()

    def uploading(self):
        global def_img
        self.filename,ok = QFileDialog.getOpenFileName(self,"upload image" ,"","Image files (*.png *.jpg) ")
        if ok:
            #print(self.filename)
            def_img = os.path.basename(self.filename)
            #print(self.filename)
            img = Image.open(self.filename)
            img.save(f"pics/{def_img}")
            self.lineEdit_12.setText(f'pics/{def_img}')

    def send_data(self):
        try:
            self.cr.execute('SELECT * FROM info')
            info = self.cr.fetchone()

            key = b'uz74glQVUR4G09H98aXDpcTliuZ1eNp2FQrPXAM0MYM='
            fernet = Fernet(key)
            with open('mail_data.json', 'rb') as file:
                original = file.read()
            decrypted = fernet.decrypt(original)
            conf = json.loads(decrypted)
            sender = conf['mail']
            password = conf['password']
            msg = MIMEMultipart("alternative")
            msg["Subject"] = " مبيعات اليوم"
            msg["From"] = sender
            msg["To"] = info[5]

            self.cr.execute('SELECT invoice FROM daily_sales WHERE id= (SELECT max(id) FROM daily_sales);')
            invoice = self.cr.fetchone()[0]

            self.cr.execute('SELECT * FROM daily_sales WHERE invoice = %s', (invoice,))
            items = self.cr.fetchall()
            table = """
                <table >
                        <thead>
                            <tr>
                                <th>العدد - </th>
                                <th>الصنف - </th>
                                <th> السعر  </th>
                            </tr>"""
            total = 0
            for item in items:
                total = total + item[4]
                table = table + f"""
                    <tr >
                        <td >{item[1]:<60} - </td>
                        <td >{item[2]:<60} - </td>
                        <td >{item[4]:<60}  </td>
                        </tr>
                        </table>"""

            html = f"""\
            <html>
                <body style="
                    align-content: center;
                    font-size: 25px;">
                    <p>{info[1]} </p>
                    <p>{invoice}</p>

                        {table}
                    <hr>
                    <p> الاجمالى:- {total}</p>
                </body>
            </html> """

            part = MIMEText(html, "html")
            msg.attach(part)

            encoders.encode_base64(part)

            # Set mail headers
            part.add_header(
                "Content-Disposition",
                "attachment",
            )
            msg.attach(part)

            # Create secure SMTP connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender, password)
                server.sendmail(
                    sender, info[5], msg.as_string()
                )

        except Exception as e:
            print(e)

    def showLastInv(self):
        self.display = invPrinter.PrintRecipt()
        self.display.show()

    def dailySalesQrShow(self):
        qr_daily_sales = QrDailySales()
        qr_daily_sales.qrdailySales()
        self.display = showQr.dailySalesQrCode()
        self.display.show()

    def showFilterSales(self):
        self.display = showFilterQr.SalesQrCode()
        self.display.show()

    def showCostQr(self):
        self.display = showQrExpense.ExpenseFilter_QrCode()
        self.display.show()


    def showInvoiceInWidget(self):
        invoice = self.label_54.text()
        self.widget_Printing.load(QtCore.QUrl.fromLocalFile(
            os.path.abspath(os.path.dirname(__file__)) + "/" + f"invoices\\invoices\\{invoice}.html"))

    def select_invoice_to_view(self):
        row = self.tableWidget_31.currentItem().row()
        receipt = self.tableWidget_31.item(row, 0).text()
        self.label_61.setText(str(receipt))
        self.tabWidget.setCurrentIndex(36)
        self.view_purchase_recipt()

    

    def print_widget(self):
        self._printer = QtPrintSupport.QPrinter()
        QPrinter.setResolution(self._printer, 800)
        self.widget_2.page().print(self._printer, self.printResult)

    def printResult(self, success):
        if success:
            print("done")
        else:
            print("print error")
        del self._printer

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == QtCore.Qt.Key_F6:
            self.insert_bar_code_for_unfounded()
        if qKeyEvent.key() == QtCore.Qt.Key_F7:
            self.tabWidget.setCurrentIndex(0)
            self.barcodeHTML()  # all barcodes
            self.updateProduct()
        
        if qKeyEvent.key() == QtCore.Qt.Key_F8:
            self.daily_export_files()

        if qKeyEvent.key() == QtCore.Qt.Key_F11:
            self.confirmPrint_2.setChecked(True)
            print('F11 clicked')
            self.printStat()
        if qKeyEvent.key() == QtCore.Qt.Key_F12:
            self.cancelPrint_2.setChecked(True)
            print('F12 clicked')
            self.printStat()

        if qKeyEvent.text() == "a" or qKeyEvent.text() == "ش":
            self.display = customer.Customer()
            self.display.show()

        if qKeyEvent.key() == QtCore.Qt.Key_F1:
            self.showLastInv()
        
        if qKeyEvent.key() == QtCore.Qt.Key_F2:
            self.home_page()

        if qKeyEvent.text() == "P":
            self.tabWidget.setCurrentIndex(28)
        if qKeyEvent.text() == "P":
            self.tabWidget.setCurrentIndex(28)
        else:
            super().keyPressEvent(qKeyEvent)

    # Start tab widgets specialized

    def admin_btn(self):
        self.tabWidget.setCurrentIndex(11)

   

    def add_category(self):
        self.tabWidget.setCurrentIndex(4)
        self.categories_in_main_window()
        self.show_all_items()


    def show_all_users(self):
        self.tabWidget.setCurrentIndex(2)
        self.get_users()

    def day_by_day_sales(self):
        self.tabWidget.setCurrentIndex(13)
        self.tabWidget_5.setCurrentIndex(0)
        self.dayByDay_sales()
        self.daily_cash()

    def add_edit_item(self):
        self.tabWidget.setCurrentIndex(3)

    def show_all_categories(self):
        self.tabWidget.setCurrentIndex(9)


    def show_reports(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(3)
        self.dashboard()
        self.all_sales()

    def show_reports_between_2_times(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(4)
        self.tabWidget_6.setCurrentIndex(1)
        self.tableWidget_26.setRowCount(0)
        self.cost_widget.setRowCount(0)

    def showCostsFilter(self):
        self.tabWidget_6.setCurrentIndex(2)

    def stock_report(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(2)
        self.get_Stock_fromDB()

    def sales_report(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(1)
        self.all_sales()

    def costs_report(self):
        self.tabWidget_4.setCurrentIndex(0)

    def analysis(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(4)
        self.tabWidget_6.setCurrentIndex(0)
        self.dashboard()

    def allprdcts(self):
        self.tabWidget.setCurrentIndex(5)
        self.showAllItems()

    def edit_delete_order(self):
        self.tabWidget.setCurrentIndex(14)

    def edituser(self):
        self.tabWidget.setCurrentIndex(11)

    def invoice_tab(self):
        self.tabWidget.setCurrentIndex(9)
        self.tabWidget_7.setCurrentIndex(0)
        self.show_invoices()

    def purchase_invoice_tab(self):
        self.tabWidget.setCurrentIndex(9)
        self.tabWidget_7.setCurrentIndex(1)
        self.show_purchase_invoice()

    def back_recipts_tab(self):
        self.tabWidget.setCurrentIndex(9)
        self.tabWidget_7.setCurrentIndex(2)
        self.show_back_recipts()

    def go_to_all_sales(self):
        self.tabWidget_5.setCurrentIndex(0)

    def go_to_all_costs(self):
        self.tabWidget.setCurrentIndex(13)
        self.tabWidget_5.setCurrentIndex(1)

    def permission_tab(self):
        self.tabWidget.setCurrentIndex(15)
        self.add_user_to_get_permissions()

    def del_user(self):
        self.tabWidget.setCurrentIndex(17)


    def printStat(self):
        if self.confirmPrint_2.isChecked():
            print("confirmed")
            self.cr.execute('UPDATE app_data SET confirm = %s ', (1,))
            self.db.commit()
        if self.cancelPrint_2.isChecked():
            self.cr.execute('UPDATE app_data SET confirm = %s ', (0,))
            self.db.commit()
        self.handlePrint()

    def handlePrint(self):
        try:
            self.cr.execute('SELECT confirm FROM app_data ')
            permission = self.cr.fetchone()[0]
            print(permission)
            if permission == 1:
                self.label_148.setStyleSheet('color: rgb(0, 255, 0);')
                self.label_148.setText('الطباعة مفعلة')
            else:
                self.label_148.setStyleSheet('color: rgb(255, 0, 0);')
                self.label_148.setText('الطباعة غير مفعلة')
        except Exception as e:
            print(e)

    def printingReciptIf(self):
        self.cr.execute('SELECT confirm FROM app_data ')
        permission = self.cr.fetchone()[0]
        print(permission)
        if permission == 1:
            self.printRecipt()
        else:
            pass

    def printRecipt(self):
        self.webEngineView = QWebEngineView()
        self.vbox.addWidget(self.webEngineView)
        self.webEngineView.load(
            QtCore.QUrl.fromLocalFile(os.path.abspath(os.path.dirname(__file__)) + "/" + "Screen\\invoice.html"))
        print("loaded receipt")

        self.webEngineView.loadFinished.connect(self.printWidget)

        self.clearCache(self.webEngineView)
        print('successfully printed')

    def printWidget(self):
        print("print_widget working")
        self._printer = QtPrintSupport.QPrinter()
        QPrinter.setResolution(self._printer, 800)
        self.webEngineView.page().print(self._printer, self.printResult)

    def clearCache(self, widget_name):
        self.widget_name = widget_name
        self.widget_name.page().profile().clearHttpCache()

    def showMostSales(self):
        self.tableWidget_13.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_13.setRowCount(0)
        self.cr.execute('''SELECT item_name ,COUNT(item_name),price FROM daily_sales
            GROUP BY item_name ORDER BY COUNT(item_name) DESC LIMIT 20;
            ''')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_13)

    def most_customer_order(self):
        self.tabWidget.setCurrentIndex(30)
        self.show_high_customers()
        
    def show_high_customers(self):
        self.tableWidget_20.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_20.setRowCount(0)
        self.cr.execute('''SELECT customer ,COUNT(item_name),SUM(total), SUM(discount) FROM daily_sales
            GROUP BY customer ORDER BY COUNT(customer) DESC LIMIT 20;
            ''')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_20)

    def show_high_customers_by_count(self):
        self.tableWidget_20.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_20.setRowCount(0)
        self.cr.execute(f'''SELECT customer ,COUNT(item_name),SUM(total), SUM(discount) FROM daily_sales
            GROUP BY customer ORDER BY COUNT(customer) DESC LIMIT {int(self.lineEdit.text())};
            ''')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_20)
    
    def showlittle_Sales(self):
        self.tableWidget_15.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget_15.setRowCount(0)
        self.cr.execute('''SELECT item_name ,COUNT(item_name),price FROM daily_sales
            GROUP BY item_name ORDER BY COUNT(item_name) ASC LIMIT 5;
            ''')
        items = self.cr.fetchall()
        FetchTables(items, self.tableWidget_15)

    def special_less_sales(self):
        try:
            number = self.lineEdit_20.text()
            self.tableWidget_15.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.tableWidget_15.setRowCount(0)
            self.cr.execute(f'''SELECT item_name ,COUNT(item_name),price FROM daily_sales
                GROUP BY item_name ORDER BY COUNT(item_name) ASC LIMIT {int(number)};''')
            items = self.cr.fetchall()
            FetchTables(items, self.tableWidget_15)

        except Exception as e:
            self.showlittle_Sales()
    
    def special_most_sales(self):
        try:
            number = self.lineEdit_18.text()
            self.tableWidget_13.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            self.tableWidget_13.setRowCount(0)
            self.cr.execute(f'''SELECT item_name ,COUNT(item_name),price FROM daily_sales
                GROUP BY item_name ORDER BY COUNT(item_name) DESC LIMIT {int(number)};''')
            items = self.cr.fetchall()
            FetchTables(items, self.tableWidget_13)

        except Exception as e:
            self.showMostSales()

    # End tab widgets specialized

    # start Handle Users
    def signUp(self):
        first_name = self.lineEdit_16.text()
        last_name = self.lineEdit_13.text()
        Phone = self.lineEdit_15.text()
        User_name = self.lineEdit_14.text()
        user_password = self.lineEdit_17.text()
        if User_name == "" or user_password == "":
            QMessageBox.about(self, 'ERROR', "رجاء ملء الحقول الفارغة")
        else:
            invoice = 0
            add_user = 0
            reports = 0
            if self.checkBox_9.isChecked():
                reports = 1
            if self.checkBox_2.isChecked():
                add_user = 1
            if self.checkBox_4.isChecked():
                invoice = 1
            self.cr.execute(f'''INSERT INTO signup(first_name ,last_name , Phone ,User_name ,user_password, reports, add_user, invoice)
                    VALUES('{first_name}' ,'{last_name}' ,'{Phone}' ,'{User_name}' ,'{user_password}','{reports}','{add_user}', '{invoice}'  )''')
            self.db.commit()
            QMessageBox.about(self, "DONE", 'تمت إضافة إسم المستخدم بنجاح')
            
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()
            self.lineEdit_15.clear()
            self.lineEdit_16.clear()
            self.lineEdit_17.clear()
            self.get_users()
            print('user added with permission')

    def get_users(self):
        self.tableWidget_18.setRowCount(0)
        self.tableWidget_18.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('''SELECT id, user_name  FROM signup''')
        users_data = self.cr.fetchall()
        self.tableWidget_18.setRowCount(len(users_data))
        for row in range(len(users_data)):
            self.btn = QtWidgets.QPushButton('')
            icon_ = QtGui.QIcon()
            icon_.addPixmap(QtGui.QPixmap(":/yellow/icons/yellow/delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.btn.setIcon(icon_)
            self.btn.setIconSize(QtCore.QSize(20, 20))
            self.btn.setStyleSheet("background-color: transparent;")
            self.tableWidget_18.setItem(row, 0, QTableWidgetItem(str((users_data[row][0]))))
            self.tableWidget_18.setItem(row, 1, QTableWidgetItem(str((users_data[row][1]))))
            self.tableWidget_18.setCellWidget(row, 2, self.btn)
            self.btn.clicked.connect(self.delete_user)
    
    def delete_user(self):
        row = self.tableWidget_18.indexAt(self.sender().pos()).row()
        id = self.tableWidget_18.item(row,0).text()
        print(id)
        areYouSure = QMessageBox()
        areYouSure.setIcon(QMessageBox.Question)
        areYouSure.setText("هل أنت متأكد من  حذف المستخدم ؟")
        areYouSure.setInformativeText(" سيتم حذف هذا المستخدم ولن يستطيع الدخول للنظام ")
        areYouSure.setWindowTitle("حذف المستخدم")
        areYouSure.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = areYouSure.exec_()
        if returnValue == QMessageBox.Yes:
            self.cr.execute("DELETE FROM signup WHERE id= %s",(id,))
            self.db.commit()
            QMessageBox.about(self, "Delete user", 'تم حذف المستخدم بنجاح')
        else:
            pass
        self.get_users()
      
    def edit_user(self):
        us_name = self.lineEdit_26.text()
        us_pasword = self.lineEdit_27.text()
        self.cr.execute('''SELECT User_name ,user_password FROM signup''')
        users = self.cr.fetchall()
        for user in users:
            user_us = user[0]
            user_ps = user[1]
            if us_name == user_us and us_pasword == user_ps:
                self.groupBox_5.setVisible(True)
            else:
                QMessageBox.warning(self, 'confirmation', 'Are you sure that\'s right? ', QMessageBox.Ok)
                # #print("not true")

    def confirm_edit_user(self):
        us_name = self.lineEdit_26.text()

        new_pass = self.lineEdit_29.text()
        if len(self.lineEdit_29.text()) < 6:
            QMessageBox.about(self, "WARNING", 'رجاء إدخال رقم سرى أكبر من 6 أحرف')
            self.lineEdit_29.clear()
        else:
            self.cr.execute(f'''UPDATE signup SET
                user_password ="{new_pass}" WHERE user_name ="{us_name}" ''')
            self.db.commit()
            QMessageBox.about(self, 'DONE', 'تم تغيير الرقم السرى بنجاح')
            self.show_all_users()
            self.groupBox_5.setVisible(False)

            self.lineEdit_26.setText("")
            self.lineEdit_27.setText("")

    def fetch_user_to_delete(self):
        code = self.lineEdit_42.text()

        self.cr.execute(f'''SELECT user_name FROM signup WHERE id = "{code}"''')
        users = self.cr.fetchall()
        for user in users:
            user_n = user[0]
            # #print(user_n)
        self.label_24.setText(f"{user_n}")

    def confirm_delete_user(self):
        code = self.lineEdit_42.text()
        self.cr.execute(f''' DELETE FROM signup WHERE id = '{code}' ''')
        self.statusBar().showMessage('''
            تتم حذف المستخدم بنجاح
            ''', 2000)

        self.lineEdit_42.setText(" ")
        self.label_24.setText(" ")

        self.get_users()


    def get_groups(self):
        groups_.clear()
        self.cr.execute('SELECT name FROM groups')
        groups = self.cr.fetchall()
        for group in groups:
            groups_.append(group[0])
    
    def showAllItems(self):
        global combo_box
        self.get_groups()
        print('groups_', groups_)
        all_items.clear()

        self.tableWidget_10.setRowCount(0)
        self.tableWidget_10.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute('''SELECT  id,name, price, groups  FROM item''')
        sales = self.cr.fetchall()
        for sale in sales:
            all_items.extend([sale])
        
        for row in range(len(all_items)):
            try:
                self.tableWidget_10.insertRow(row)
                self.btn = QPushButton("نحميل صورة")
                combo_box = QtWidgets.QComboBox()
                combo_box.clear()
                combo_box.addItems(groups_)
                combo_box.setCurrentText(str(all_items[row][3]))
                
                self.tableWidget_10.setItem(row, 0, QTableWidgetItem(str(all_items[row][0])))
                self.tableWidget_10.setItem(row, 1, QTableWidgetItem(str(all_items[row][1])))
                self.tableWidget_10.setItem(row, 2, QTableWidgetItem(str(all_items[row][2])))
                self.tableWidget_10.setCellWidget(row, 3, combo_box)
                self.tableWidget_10.setCellWidget(row, 4, self.btn)

                combo_box.currentIndexChanged.connect(self.handle_combo)
                self.btn.clicked.connect(self.change_image)
            except Exception as e:
                print(e)
    
    def change_image(self):
        try:
            row = self.tableWidget_10.indexAt(self.sender().pos()).row()
            item_code = self.tableWidget_10.item(row,0).text()
            print(item_code)

            self.filename,ok = QFileDialog.getOpenFileName(self,"upload image" ,"","Image files (*.png *.jpg) ")
            if ok:
                def_img = os.path.basename(self.filename)
                img = Image.open(self.filename)
                img.save(f"pics/{def_img}")
                self.cr.execute(f' UPDATE item SET image = "pics/{def_img}" WHERE id ="{item_code}" ')
                self.db.commit()
                QMessageBox.about(self,"Done", "تمت الاضافة بنجاح" )

        except Exception as e:
            print(e)


    def handle_combo(self):
        try:
            combo_ = self.sender()
            index = self.tableWidget_10.indexAt(combo_.pos())
            new_group = combo_.currentText()
            if index.isValid():
                print(index)
                print(combo_box.currentText())
                self.cr.execute("UPDATE item SET  groups = %s WHERE id LIKE %s ",( new_group, self.tableWidget_10.item(index.row(),0).text(),))
                print('updated')
                self.db.commit()
        except AttributeError:
            pass
        except Exception as e:
            print(e)
    
    def handle_combo_cell_edit(self):
        try:
            row_ = self.tableWidget_10.currentItem().row()
            print(row_)
            name = self.tableWidget_10.item(row_, 1).text()
            price = self.tableWidget_10.item(row_, 2).text()
            
            self.cr.execute("UPDATE item SET  name = %s, price = %s WHERE id LIKE %s ",( name, price, self.tableWidget_10.item(row_, 0).text(),))
            print('updated 2')
            self.db.commit()
        except TypeError:
            pass
        except Exception as s:
            print(s)

    def disable_btn(self):
        self.lineEdit_10.textChanged.connect(self.on_text_changed)

    @QtCore.pyqtSlot()
    def on_text_changed(self):
        self.pushButton_23.setEnabled(bool(self.lineEdit_10.text()))


    # end disable / enable button depend on entry fields

    # start handling costs


    def all_costs(self):
        self.cr.execute('''SELECT  name , price ,date FROM expense''')
        costs_data = self.cr.fetchall()
        set_default = []
        for a in costs_data:
            pric = a[1]  # price column in table
            set_default.append(pric)
        costs = sum(set_default)
        self.label_4.setText(str(round(costs, 2)))
        self.label_38.setText(f'{costs}')


    def expense2edit(self):
        row = self.tableWidget_6.currentItem().row()
        print(row)
        name = self.tableWidget_6.item(row, 0).text()
        edited_date = self.tableWidget_6.item(row, 3).text()

        print(name, edited_date)

        self.cr.execute(
            f'''SELECT  name , price ,status, id FROM expense WHERE name = '{name}' AND date = "{edited_date}" ''')
        data_ = self.cr.fetchone()
        print(data_)
        self.widget_3.setVisible(True)
        self.lineEdit_55.setText(str(data_[0]))
        self.lineEdit_56.setText(str(data_[1]))
        self.comboBox_4.setCurrentText(str(data_[2]))
        self.label_69.setText(str(data_[3]))

    def updateExpense(self):
        code = self.label_69.text()
        name = self.lineEdit_55.text()
        price = self.lineEdit_56.text()
        status = self.comboBox_4.currentText()
        prod_image = def_img
        self.cr.execute(f'''UPDATE expense SET name = '{name}' ,
            price = '{price}' , status = '{status}' WHERE id = "{code}" ''')
        self.db.commit()
        print(prod_image)

        self.tableWidget_6.setRowCount(0)
        self.get_costs_fromDB()

        self.tableWidget_4.setRowCount(0)
        self.get_Stock_fromDB()

        self.tableWidget_7.setRowCount(0)
        self.not_stock_costs()

        self.tableWidget_23.setRowCount(0)
        self.daily_Expense()
        self.daily_cash()
        self.show_invoices()

        self.label_69.setText("")
        self.lineEdit_55.clear()
        self.lineEdit_56.clear()
        self.comboBox_4.setCurrentIndex(0)

    # end handling costs

    def validator(self):
        # To allow only int and float
        self.onlyInt = QIntValidator()
        self.lineEdit_10.setValidator(self.onlyInt)
        # self.lineEdit_56.setValidator(self.onlyInt)
        # self.lineEdit_8.setValidator(self.onlyInt)
        # self.lineEdit_70.setValidator(self.onlyInt)
        # self.lineEdit_18.setValidator(self.onlyInt)
        
        # self.lineEdit_18.setValidator(QDoubleValidator(9999, -9999, 4))
        self.lineEdit_10.setValidator(QDoubleValidator(9999, -9999, 4))
        # self.lineEdit_8.setValidator(QDoubleValidator(9999, -9999, 4))
        # self.lineEdit_56.setValidator(QDoubleValidator(9999, -9999, 4))
        # self.lineEdit_70.setValidator(QDoubleValidator(9999, -9999, 4))


    def purchase_recipt_search(self):
        value = self.invSearchlineEdit_2.text()
        if value == "":
            self.show_purchase_invoice()
        else:
            query = """SELECT recipt, item, item_price, count, total, date FROM purchase_recipt
                WHERE recipt LIKE %s or item LIKE %s"""
            self.cr.execute(query, ('%' + value + '%', '%' + value + '%'))
            result = self.cr.fetchall()
            if not result:
                self.show_purchase_invoice()
            else:
                self.template_search(self.tableWidget_31, result)

    def categories_in_main_window(self):
        self.cr.execute(f'SELECT name FROM groups ')
        s= self.cr.fetchall()
        print(s)
        positions = [(i,j) for i in range(len(s)) for j in range(3)]
        for position, name in zip(positions, s):

            button = QPushButton(f'{name[0]}')
            
            button.setBaseSize(200,200)
            button.setStyleSheet("*{\n"
                "    color: rgb(0, 0, 0);\n"
                "    height:45px;\n"
                "    width:70px;\n"
                "    font: 18pt \"Shorooq_N1\";"
                "}\n"
                "\n"
                "QPushButton:hover{\n"
                "    \n"
                "    \n"
                "    background-color: rgb(77, 50, 247);\n"
                "    padding:6px 6px;\n"
                "    border-top-left-radius:17px;\n"
                "    border-color: rgb(0, 85, 127);\n"
                "    color: rgb(255, 255, 255);\n"
                "}\n")
            self.gridLayout_53.addWidget(button,*position,1,1)
            button.clicked.connect(self.handle_show_group)

    def handle_show_group(self):
        self.tabWidget_9.setCurrentIndex(1)
        self.group_lbl.setText(self.sender().text())
        print(self.sender().text())
        try :
            self.cr.execute(f'''SELECT name,price FROM items WHERE groups = "{self.sender().text()}" ''')
            item= self.cr.fetchall()
            print(item)

            self.clearLayout(self.gridLayout_55)
            self.tabWidget.setCurrentIndex(4)
            positions = [(i,j) for i in range(len(item)) for j in range(2 )]
            for position, name in zip(positions, item):
                self.frame = QtWidgets.QFrame()        
                self.button = QPushButton()
                self.button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "height:50px;  \n"
                "font: 18pt \"Shorooq_N1\"; "
                )
                # 
                self.button.setText(f"{name[0]}")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
                self.frame.setSizePolicy(sizePolicy)
                self.VLayout = QtWidgets.QVBoxLayout(self.frame)
                self.VLayout.setContentsMargins(20, 10, 20, 10)
                self.VLayout.addWidget(self.button)

                self.gridLayout_55.addWidget(self.frame,*position,1,1)
                self.button.clicked.connect(self.addem)

        except Exception as e:
            print(e)
    
    def show_all_items(self):
        try :
            self.cr.execute('SELECT name,price,image FROM item ')
            item= self.cr.fetchall()
            print(item)

            self.clearLayout(self.gridLayout)
            self.tabWidget.setCurrentIndex(4)
            positions = [(i,j) for i in range(len(item)) for j in range(5)]
            for position, name in zip(positions, item):
                self.frame = QtWidgets.QFrame()
                self.frame.setFixedSize(260,230)
                self.pixmap = QPixmap(name[2])
                
                self.label = QLabel()
                self.label.setPixmap(self.pixmap)
                self.label.setScaledContents(True)
                self.button = QPushButton()
                self.button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "height:50px;  \n"
                "font: 20pt \"Shorooq_N1\"; "
                )
                # 
                self.button.setText(f"{name[0]}")
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
                self.frame.setSizePolicy(sizePolicy)
                self.VLayout = QtWidgets.QVBoxLayout(self.frame)
                # self.VLayout.setSizeConstraint(180,170)
                self.VLayout.setContentsMargins(20, 10, 20, 10)
                self.VLayout.addWidget(self.label)
                self.VLayout.addWidget(self.button)

                self.gridLayout.addWidget(self.frame,*position,1,1)
                self.button.clicked.connect(self.addem_all_items)



        except Exception as e:
            print(e)


    def clearLayout(self, layout):
        self.gridLayout = layout
        if self.gridLayout is not None:
            while self.gridLayout.count():
                item = self.gridLayout.takeAt(0)
                self.widget_2 = item.widget()
                if self.widget_2 is not None:
                    self.widget_2.deleteLater()
                else:
                    self.clearLayout(item.gridLayout())

    def add_items(self):
        try:
            if self.lineEdit_72.text() == " ":
                QMessageBox.information(self, "warning", "لابد من إستكمال البيانات الناقصة")
            else:
                self.cr.execute(f'''INSERT INTO item( name , price, groups ,image)VALUES('{self.lineEdit_72.text()}',
                "{self.lineEdit_8.text()}", "{self.comboBox.currentText()}", "{self.lineEdit_12.text()}")
                ''')
                self.db.commit()
                self.lineEdit_72.clear()
                self.lineEdit_8.clear()
                self.lineEdit_12.clear()
                self.comboBox.setCurrentIndex(0)

                QMessageBox.information(self, "success", " تمت الاضافة بنجاح")
        except Exception as e:
            QMessageBox.information(self, "warning", str(e))


    def cleanorder(self):
        self.tableWidget_12.setRowCount(0)
        self.label_2.setText("0")
        self.lineEdit_36.clear()

    def between_dates_activities(self):
        self.tableWidget_9.setRowCount(0)
        self.tableWidget_9.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cr.execute(f'''SELECT id, trainer, category, start, coach, date FROM activity WHERE date BETWEEN 
            '{self.dateEdit.date().toPyDate()}' AND '{self.dateEdit_2.date().toPyDate()}' ''')
        months = self.cr.fetchall()
        FetchTables(months, self.tableWidget_9)


    def filter_discounts(self):
        total = []
        try:
            self.cr.execute(f'''SELECT discount from daily_sales WHERE
            date BETWEEN '{self.dateEdit.date().toPyDate()}' AND '{self.dateEdit_2.date().toPyDate()}' ''')
            discounts = self.cr.fetchall()

            for discount in discounts:
                total.append(discount[0])
            all_discounts = sum(total)
            return str(all_discounts)
        except TypeError as s:
            print(s)
            return "0"

        except Exception as e:
            print(str(e))

    def generateQrCodeReport(self):
        GenetateQrCode = QrDashboard()
        GenetateQrCode.qrReportMaker()
        self.showQrReport()

    def showQrReport(self):
        self.display = showReportQrCode.ReportQrCode()
        self.display.show()

    def filterCosts(self):
        self.cost_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cost_widget.setRowCount(0)
        fil_year = self.dateEdit_2.date()
        filter_year = fil_year.toPyDate()
        first = self.dateEdit.date()
        filter_first = first.toPyDate()
        from_ = str(filter_first)
        to_ = str(filter_year)

        generate_cost_filter = GernerateCostsFilter()
        generate_cost_filter.generateQr_costFilter(from_, to_)

        self.cr.execute(f'''SELECT id ,name, price , status , date from expense
            WHERE date BETWEEN '{from_}' AND '{to_}' ''')

        months = self.cr.fetchall()
        FetchTables(months, self.cost_widget)
        total = []
        for x in months:
            price = x[2]
            total.append(price)

        sumFilter = sum(total)
        self.label_56.setText(str(math.ceil(sumFilter)))

    # End handle daily orders

    # Daily Sales
    def dayByDay_sales(self):

        self.tableWidget_22.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableWidget_22.setRowCount(0)

        self.cr.execute(
            f'''SELECT id,count ,item_name,price,total,discount FROM daily_sales WHERE date ="{date.today().strftime("%Y-%m-%d")}"  ''')
        day_sale = self.cr.fetchall()
        FetchTables(day_sale, self.tableWidget_22)

        self.cr.execute(f'''SELECT id,count ,item_name,price,total FROM daily_sales
            WHERE date ="{date.today().strftime("%Y-%m-%d")}"  ''')
        day_sale = self.cr.fetchall()
        total_today_sales = 0
        for x in day_sale:
            total_today_sales =total_today_sales + x[4]


        all_day = int(total_today_sales) - int(self.count_discount())
        self.label_17.setText(f"{int(all_day)}")

        self.label_28.setText(str(self.count_discount()))

    def count_discount(self):
        total = 0
        try:
            self.cr.execute(f'SELECT discount from daily_sales WHERE date ="{date.today().strftime("%Y-%m-%d")}" ')
            discounts = self.cr.fetchall()

            for discount in discounts:
                total = total+ discount[0]
            return str(total)
        except TypeError as s:
            print(s)
            return "0"

        except Exception as e:
            print(str(e))


    def daily_cash(self):
        self.cr.execute(f'''SELECT price FROM daily_sales
            WHERE start_date ="{date.today().strftime("%Y-%m-%d")}"  ''')
        day_sale = self.cr.fetchall()
        total_today_sales = []
        for x in day_sale:
            now_sales = x[0]
            total_today_sales.append(now_sales)

        all_day = sum(total_today_sales)

    # End Daily Sales

    # Daily Expense
    def daily_Expense(self):
        self.tableWidget_23.setRowCount(0)
        self.tableWidget_23.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.cr.execute(
            f'''SELECT  name , price ,status, date FROM expense WHERE date ="{date.today().strftime("%Y-%m-%d")}" ''')
        day_expense = self.cr.fetchall()
        FetchTables(day_expense, self.tableWidget_23)
        total_expense = []
        for x in day_expense:
            pay = x[1]
            total_expense.append(pay)
        self.cr.execute(f'SELECT paid FROM recipt_pay WHERE pay_date ="{date.today().strftime("%Y-%m-%d")}" ')
        ps = []
        paids = self.cr.fetchall()
        for p in paids:
            ps.append(p[0])

    # end handle daily expense

    # start all sales
    def all_sales(self):
        self.tableWidget_21.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableWidget_21.setRowCount(0)
        self.cr.execute(f'''SELECT id,count ,item_name,price,total,date ,stat FROM daily_sales''')
        all_items = self.cr.fetchall()
        FetchTables(all_items, self.tableWidget_21)

        total = []
        for item in all_items:
            price = item[4]
            total.append(price)

        cost = float(sum(total))

        self.label.setText(f"{math.ceil(cost)}")
        self.allSalesLabel.setText(f"{round(cost, 1)}")

    # end all sales


    # Export to Excel sheet
    def export_file(self):  # Sales Files

        self.cr.execute('SELECT id,count ,item_name,price,total,date FROM daily_sales ')
        data_ = self.cr.fetchall()
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            sheet = file.add_worksheet()

            sheet.write(0, 0, "الكود")
            sheet.write(0, 1, "العدد")
            sheet.write(0, 2, "الصنف")
            sheet.write(0, 3, "السعر")
            sheet.write(0, 4, "اجمالى السعر")
            sheet.write(0, 5, "التاريخ")

            row_number = 1
            for row in data_:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            file.close()
        except:
            print('you didn\'t save file ')

    def export_purchase_recipt(self):
        self.cr.execute(f''' SELECT recipt, item, item_price, count, total, date from purchase_recipt   ''')
        stock_costs = self.cr.fetchall()
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            sheet = file.add_worksheet()
            sheet.write(0, 0, "رقم الفاتورة")
            sheet.write(0, 1, "الصنف")
            sheet.write(0, 2, "سعر الصنف")
            sheet.write(0, 3, "العدد")
            sheet.write(0, 4, "اجمالى")
            sheet.write(0, 5, "التاريخ")

            row_number = 1
            for row in stock_costs:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            file.close()
        except:
            print('you didn\'t save file ')

    def export_notstock(self):
        stock_items = "مخزن"
        self.cr.execute(f''' SELECT name , price ,date FROM expense WHERE status != '{stock_items}' ''')
        stock_costs = self.cr.fetchall()

        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            sheet = file.add_worksheet()

            sheet.write(0, 0, "الصنف")
            sheet.write(0, 1, "السعر")
            sheet.write(0, 2, "التاريخ")

            row_number = 1
            for row in stock_costs:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            file.close()
        except:
            print('you didn\'t save file ')

    def export_monthByMonth(self):
        self.cr.execute(
            f'''SELECT id,count,item_name, price, total, date from daily_sales WHERE
                date BETWEEN '{self.dateEdit.date().toPyDate()}' AND '{self.dateEdit_2.date().toPyDate()}' ''')
        months = self.cr.fetchall()
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            sheet = file.add_worksheet()
            cells = file.add_format()
            cells.set_font_size(13)
            cells.set_bold()
            cells.set_align('center')
            cells.set_border()

            date_time = datetime.strptime(str(date.today()),'%Y-%m-%d')
            date_format = file.add_format({'num_format': "d mmmm yyy",
                                    'align': 'center',
                                    'font_size':14,
                                    })
            sheet.write_datetime(0,2, date_time, date_format)
            sheet.set_column('C:C', 16)
            sheet.merge_range('C2:E3','مبيعات فترة زمنية', cells)
            sheet.write(3,2,f"{self.dateEdit.date().toPyDate()}", cells)
            sheet.merge_range('D4:E4',f'{self.dateEdit_2.date().toPyDate()}', cells)
            sheet.write(4, 0, "مسلسل",cells )
            sheet.write(4, 1, "كمية",cells)
            sheet.write(4, 2, "الصنف",cells)
            sheet.write(4, 3, "السعر",cells)
            sheet.write(4, 4, "الاجمالي",cells)
            sheet.write(4, 5, "التاريخ",cells)

            row_number = 5
            for row in months:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            file.close()
        except Exception as e:
            print(e)

            print('you didn\'t save file ')

    def export_filterCosts(self):
        fil_year = self.dateEdit_2.date()
        filter_year = fil_year.toPyDate()
        first = self.dateEdit.date()
        filter_first = first.toPyDate()
        from_ = str(filter_first)
        to_ = str(filter_year)

        self.cr.execute(f'''SELECT id ,name , price , status , date from expense
            WHERE date BETWEEN '{from_}' AND '{to_}' ''')

        months = self.cr.fetchall()
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            sheet = file.add_worksheet()
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "الاسم")
            sheet.write(0, 2, "السعر")
            sheet.write(0, 3, "الحالة")
            sheet.write(0, 4, "التاريخ")

            row_number = 1
            for row in months:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            file.close()
        except:
            print('you didn\'t save file ')

    # End Export to Excel sheet

    def back_up(self):
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xlsx(*.xlsx)")
            file = Workbook(filename)
            # daily sales
            self.cr.execute(f'''SELECT id ,count,item_name ,price ,total, discount,invoice ,date FROM daily_sales''')
            sales = self.cr.fetchall()
            sheet = file.add_worksheet('إجمالى المبيعات')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "العدد")
            sheet.write(0, 2, "الصنف")
            sheet.write(0, 3, "السعر")
            sheet.write(0, 4, "الاجمالى")
            sheet.write(0,5,"الخصم")
            sheet.write(0, 6, "الفاتورة")
            sheet.write(0, 7, "التاريخ")

            row_number = 1
            for row in sales:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            # items
            self.cr.execute(f'''SELECT id ,name , price, groups FROM item''')

            items = self.cr.fetchall()
            sheet1 = file.add_worksheet('الاصناف')
            sheet1.write(0, 0, "مسلسل")
            sheet1.write(0, 1, "الصنف")
            sheet1.write(0, 2, "السعر")
            sheet1.write(0, 3, "التصنيف")

            row_number = 1
            for row in items:
                column_number = 0
                for item in row:
                    sheet1.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            # expense
            self.cr.execute(f'''SELECT id ,name ,price ,status ,date FROM expense''')
            ex = self.cr.fetchall()
            sheet = file.add_worksheet('إجمالى المصروفات')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "الاسم")
            sheet.write(0, 2, "السعر")
            sheet.write(0, 3, "نوع المصروفات")
            sheet.write(0, 4, "التاريخ")

            row_number = 1
            for row in ex:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            
            # debts for purchases
            self.cr.execute(f'''SELECT id ,name ,invoice ,total ,paid ,remain,invoice_date FROM recipts''')
            dbts = self.cr.fetchall()
            sheet = file.add_worksheet(' المستحق للتجار  ')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "اسم التاجر")
            sheet.write(0, 2, "الفاتورة")
            sheet.write(0, 3, "الاجمالى")
            sheet.write(0, 4, "المدفوع")
            sheet.write(0, 5, "المتبقى")
            sheet.write(0, 6, "التاريخ")
            row_number = 1
            for row in dbts:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            # paids for purchases
            self.cr.execute(f'''SELECT id ,name ,invoice ,total ,paid ,remain,pay_date FROM recipt_pay''')
            buydbts = self.cr.fetchall()
            sheet = file.add_worksheet(' دفعات للتجار  ')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "اسم التاجر")
            sheet.write(0, 2, "الفاتورة")
            sheet.write(0, 3, "الاجمالى")
            sheet.write(0, 4, "المدفوع")
            sheet.write(0, 5, "المتبقى")
            sheet.write(0, 6, "التاريخ")
            row_number = 1
            for row in buydbts:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            file.close()
            QMessageBox.about(self, "Done", 'Back up file export successfully')
            SendBackup()
        except Exception as e:
            print(str(e))
            # QMessageBox.warning(self, "Warning", "لم تقم بإستيراد الملفات ")

    # START DASH BOARD FOR REPORTS
    def report_total_sales(self):
        totalSales_ = 0
        try:
            self.cr.execute(f'''SELECT total FROM daily_sales''')
            all_items = self.cr.fetchall()
            for item in all_items:
                price = item[0]
                totalSales_ = totalSales_ + price
            return '{:.1f}'.format(totalSales_)

        except Exception as e:
            print(e, '==> report_total_sales')
            return '0'

    def report_remain(self):
        try:
            remain_ = 0
            self.cr.execute('SELECT remain FROM salesDebts ')
            remains = self.cr.fetchall()
            for n in remains:
                sal = n[0]
                remain_ = remain_ + sal
            return '{:.1f}'.format(remain_)
        except Exception as e:
            print(e)
            return 'Error'

    def report_income_sales(self):
        income = 0
        try:
            self.cr.execute(f'SELECT total FROM daily_sales ')
            sales = self.cr.fetchall()
            for sale in sales:
                total_income = sale[0]
                income = income + total_income
            return '{:.1f}'.format(income)
        except:
            return '0'

    def report_debts_paid(self):
        debts_paids = 0
        self.cr.execute(f'SELECT paid from recipts')
        paids = self.cr.fetchall()
        for paid in paids:
            debts_paids = debts_paids + paid[0]
        return '{:.1f}'.format(debts_paids)

    def report_expense_price(self):
        try:
            total = 0
            self.cr.execute(f''' SELECT price FROM expense ''')
            prices = self.cr.fetchall()
            for price in prices:
                total = total + price[0]
            return total
        except:
            return "0"

    def report_debts_remains(self):
        try:
            debts_remains = 0
            self.cr.execute('SELECT remain FROM recipts')
            remains = self.cr.fetchall()
            for r in remains:
                debts_remains = debts_remains + r[0]
            return "{:.1f}".format(debts_remains)
        except:
            return "0"

    def dashboard(self):

        self.widget.clear()
        self.label_121.setText(str(self.discounts()))
        all_expense = float(self.report_expense_price()) + float(self.report_debts_paid())
        self.totalCostLabel.setText(str(all_expense))
        self.debtLabel.setText(str(self.report_debts_remains()))
        x1, x2, x4, x5 = [1], [2], [4], [5]
        
        data1 = pg.BarGraphItem(x=x1, height=float(self.report_income_sales()), width=.4, brush='g')
        self.widget.addItem(data1)
        data_ = pg.BarGraphItem(x=x2, height=all_expense, width=.4, brush='r')
        self.widget.addItem(data_)

        data3 = pg.BarGraphItem(x=x4, height=float(self.report_debts_remains()), width=.4, brush='y')
        self.widget.addItem(data3)
        data4 = pg.BarGraphItem(x=x5, height=float(self.report_remain()), width=.4, brush='k')
        self.widget.addItem(data4)
        self.widget.setTitle("تقرير ")
        self.widget.setBackground("w")
        self.widget.setLabel("left", "horizontal", color="red", size='50')
        self.widget.showGrid(x=False, y=True)


    # END DASH BOARD FOR REPORTS
    # user permissions
    def add_user_to_get_permissions(self):
        """" every time you click permission tab username add to combo box"""
        self.comboBox_7.clear()
        self.cr.execute('SELECT user_name ,user_password FROM signup ')
        users = self.cr.fetchall()
        for user in users:
            self.comboBox_7.addItem(user[0])

    def user_permissions(self):

        name = self.comboBox_7.currentText()

        self.cr.execute(f'DELETE FROM permissions WHERE name = "{name}"')

        if self.checkBox_12.isChecked():
            self.cr.execute(''' INSERT INTO permissions(name ,addItem ,stock ,home ,dailySales ,reports ,
            expense,customerPayment ,invoices ,editOrder ,supplierPayment ,editDeleteItem ,payLater , admin , make_order)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (name, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))

            self.db.commit()
        else:
            addItem = 0
            stock = 0
            home = 0
            dailySales = 0
            reports = 0
            expense = 0
            customerPayment = 0
            invoices = 0
            editOrder = 0
            supplierPayment = 0
            editDeleteItem = 0
            payLater = 0
            admin = 0
            make_order = 0

            # conditions
            if self.checkBox.isChecked():
                addItem = 1
            if self.checkBox_11.isChecked():
                stock = 1
            if self.checkBox_13.isChecked():
                home = 1
            if self.checkBox_5.isChecked():
                dailySales = 1
            if self.checkBox_6.isChecked():
                reports = 1
            if self.checkBox_10.isChecked():
                expense = 1
            if self.checkBox_3.isChecked():
                customerPayment = 1
            if self.checkBox_29.isChecked():
                invoices = 1
            if self.checkBox_14.isChecked():
                editOrder = 1
            if self.checkBox_8.isChecked():
                supplierPayment = 1
            if self.checkBox_15.isChecked():
                editDeleteItem = 1
            if self.checkBox_7.isChecked():
                payLater = 1
            if self.checkBox_12.isChecked():
                admin = 1
            if self.checkBox_13.isChecked():
                make_order = 1
            # conditions
            self.cr.execute(f''' INSERT INTO permissions(name, addItem, stock, home, dailySales, reports, 
                expense, customerPayment, invoices, editOrder, supplierPayment, editDeleteItem, payLater, admin,
                make_order) VALUES("{name}","{addItem}" ,"{stock}" ,"{home}" ,"{dailySales}","{reports}" ,"{expense}",
                "{customerPayment}" ,"{invoices}" ,"{editOrder}" ,"{supplierPayment}" ,"{editDeleteItem}" ,"{payLater}", "{admin}" ,"{make_order}") 
            ''')
            self.db.commit()
            QMessageBox.information(self, "Done", "تمت إضافة الصلاحيات للمستخدم بنجاح ")

    def daily_export_files(self):
        try:
            self.cr.execute(f'''SELECT invoice ,name, phone , groups , package , count, price, start_date, finish  FROM daily_sales
                WHERE start_date = "{date.today().strftime("%Y-%m-%d")}"
            ''')
            sales = self.cr.fetchall()
            file = Workbook('يومية.xlsx')
            sheet = file.add_worksheet('الاشتراكات')
            sheet.write(0, 0, "فاتورة")
            sheet.write(0, 1, "المشترك")
            sheet.write(0, 2, "الهاتف")
            sheet.write(0, 3, "الفئة")
            sheet.write(0, 4, "الباقة")
            sheet.write(0, 5, "عدد التمارين")
            sheet.write(0, 6, "القيمة ")
            sheet.write(0, 7, "تاريخ البدء ")
            sheet.write(0, 8, "نهاية الاشتراك ")

            row_number = 1
            for row in sales:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            self.cr.execute(f'SELECT id, name, price, status, date FROM expense WHERE date = "{date.today().strftime("%Y-%m-%d")}"')
            purchases = self.cr.fetchall()
            sheet1 = file.add_worksheet('المصروفات')
            sheet1.write(0, 0, "م")
            sheet1.write(0, 1, "البيان")
            sheet1.write(0, 2, "سعر ")
            sheet1.write(0, 3, "الوصـف")
            sheet1.write(0, 4, "التاريخ")

            row_number = 1
            for row in purchases:
                column_number = 0
                for item in row:
                    sheet1.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            self.cr.execute(f'SELECT id, trainer, category, coach, start, date FROM activity WHERE date = "{date.today().strftime("%Y-%m-%d")}" ')
            backs = self.cr.fetchall()

            sheet2 = file.add_worksheet('نشاط اليوم')
            sheet2.write(0,0,"م")
            sheet2.write(0,1,"مشترك")
            sheet2.write(0,2, "الفئة")
            sheet2.write(0,3,"المدرب")
            sheet2.write(0,4,"وقت البدء")
            sheet2.write(0,5,"التاريخ")

            row_number = 1
            for row in backs:
                column_number = 0
                for item in row:
                    sheet2.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            file.close()
        except Exception as e:
            print(e)

    def all_export_files(self):
        try:
            self.cr.execute(f'''SELECT invoice ,name, phone , groups , package , count, price, start_date, finish  FROM daily_sales''')
            sales = self.cr.fetchall()
            file = Workbook('اجمالى.xlsx')
            sheet = file.add_worksheet('الاشتراكات')
            sheet.write(0, 0, "فاتورة")
            sheet.write(0, 1, "المشترك")
            sheet.write(0, 2, "الهاتف")
            sheet.write(0, 3, "الفئة")
            sheet.write(0, 4, "الباقة")
            sheet.write(0, 5, "عدد التمارين")
            sheet.write(0, 6, "القيمة ")
            sheet.write(0, 7, "تاريخ البدء ")
            sheet.write(0, 8, "نهاية الاشتراك ")

            row_number = 1
            for row in sales:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            self.cr.execute(f'SELECT id, name, price, status, date FROM expense ')
            purchases = self.cr.fetchall()
            sheet1 = file.add_worksheet('المصروفات')
            sheet1.write(0, 0, "م")
            sheet1.write(0, 1, "البيان")
            sheet1.write(0, 2, "سعر ")
            sheet1.write(0, 3, "الوصـف")
            sheet1.write(0, 4, "التاريخ")

            row_number = 1
            for row in purchases:
                column_number = 0
                for item in row:
                    sheet1.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1

            self.cr.execute(f'SELECT id, trainer, category, coach, start, date FROM activity')
            backs = self.cr.fetchall()

            sheet2 = file.add_worksheet('نشاط اليوم')
            sheet2.write(0,0,"م")
            sheet2.write(0,1,"مشترك")
            sheet2.write(0,2, "الفئة")
            sheet2.write(0,3,"المدرب")
            sheet2.write(0,4,"وقت البدء")
            sheet2.write(0,5,"التاريخ")

            row_number = 1
            for row in backs:
                column_number = 0
                for item in row:
                    sheet2.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            file.close()
        except Exception as e:
            print(e)

    def send_daily_data_(self):
        self.daily_export_files()
        self.all_export_files()
        self.cr.execute('SELECT mail FROM app_data')
        receivers = self.cr.fetchone()[0]
        key = b'uz74glQVUR4G09H98aXDpcTliuZ1eNp2FQrPXAM0MYM='
        fernet = Fernet(key)
        with open('mail_data.json', 'rb') as file:
            original = file.read()
        decrypted = fernet.decrypt(original)
        conf = json.loads(decrypted)
        print(conf)
        sender = conf['mail']
        password = conf['password']

        msg = MIMEMultipart("alternative")
        msg["Subject"] = f" ملخص يوم {date.today().strftime('%Y:%m:%d')}"
        msg["From"] = sender
        msg["To"] = receivers
        filenames = ['يومية.xlsx','اجمالى.xlsx','sports.sql']

        # HTML Message Part
        html = """\
        <html>
            <body>
            <h1>أوج لحلول الأعمال</h1>
            <br>
            <h2>
               Click on <a href="https://fb.com/awgsolutions">Awg for Business solutions</a> 
               for contact with us.
            
            </h2>
          </body>
        </html>
        """

        part = MIMEText(html, "html")
        msg.attach(part)

        # Add Attachment
        for file in filenames :
            with open(file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            # Set mail headers
            part.add_header(
                "Content-Disposition",
                "attachment", filename=file
            )
            msg.attach(part)

        # Create secure SMTP connection and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receivers, msg.as_string())

        print('sent to '+ receivers)
    
    def export_sql(self):
        try:
            self.cr.execute('SELECT db_path FROM app_data ')
            path = self.cr.fetchone()[0]
            a = ExportBackUp()
            a.export_sql(path.replace('\\','/'))
        except Exception as ex:
            QMessageBox.about(self, 'warning',str(ex) )
    
    def closeEvent(self, event):
        close = QMessageBox.question(self, "خروج", "أنت على وشك الخروج من النظام .. اضغط yes لحفظ البيانات والخروج",
                                    QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            self.export_sql()
            self.send_daily_data_()
            event.accept()
            print('closed')
        else:
            self.export_sql()
            event.ignore()


def main():
    app = QApplication(sys.argv)
    window = Signing()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
