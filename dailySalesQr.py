import sqlite3
import qrcode
from datetime import date
from prettytable import PrettyTable


def qrdailySales():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
        )
    db = sqlite3.connect('businessdata.db')
    cr = db.cursor()
    time_= date.today()
    today = time_.strftime("%Y-%m-%d")
    cr.execute(f'''SELECT count ,item_name,price,total,stat FROM daily_sales
                WHERE date ="{today}"  ''')
    Sales = cr.fetchall()
    myTable =PrettyTable(['العدد','الصنف',' السعر','الاجمالي','الحالة'])
    for row in Sales:
        myTable.add_row([row[0],row[1],row[2],row[3],row[4]])

    qr.add_data(myTable)
    qr.make(fit = True)

    img = qr.make_image()
    img.save(f"qr/daySales/daysales.jpg")
