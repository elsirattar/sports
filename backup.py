from xlsxwriter import *
from encrypted import Connection


class ExportAll(Connection):
    def __init__(self):
        self.cr = None
        self.db = None
        self.connector()
        self.back_up()

    def back_up(self):
        try:
            file = Workbook('backup.xlsx')
            # daily sales
            self.cr.execute(f'''SELECT id ,count,item_name ,price ,total,stat,invoice ,profit ,date FROM daily_sales''')
            sales = self.cr.fetchall()
            sheet = file.add_worksheet('إجمالى المبيعات')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "العدد")
            sheet.write(0, 2, "الصنف")
            sheet.write(0, 3, "السعر")
            sheet.write(0, 4, "الاجمالى")
            sheet.write(0, 5, "الحالة")
            sheet.write(0, 6, "الفاتورة")
            sheet.write(0, 7, "الارباح")
            sheet.write(0, 8, "التاريخ")

            row_number = 1
            for row in sales:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            # items
            self.cr.execute(f'''SELECT id ,name , count ,price ,item_price ,code,expire, stock FROM item''')

            items = self.cr.fetchall()
            sheet1 = file.add_worksheet('الاصناف')
            sheet1.write(0, 0, "مسلسل")
            sheet1.write(0, 1, "الصنف")
            sheet1.write(0, 2, "العدد")
            sheet1.write(0, 3, "السعر")
            sheet1.write(0, 4, "الجملة")
            sheet1.write(0, 5, "الكود")
            sheet1.write(0, 6, "تاريخ الصلاحية")
            sheet1.write(0, 7, "المخزن")

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

                # sales debts
            self.cr.execute(f'''SELECT id ,invoice,name ,phone ,paid ,allMoney,remain,date FROM salesDebts''')
            salesDebts = self.cr.fetchall()
            sheet = file.add_worksheet('العملاء المديونين ')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "الفاتورة")
            sheet.write(0, 2, "الاسم")
            sheet.write(0, 3, "الهاتف")
            sheet.write(0, 4, "المدفوع")
            sheet.write(0, 5, "الإجمالى")
            sheet.write(0, 6, "المتبقى")
            sheet.write(0, 7, "التاريخ")
            row_number = 1
            for row in salesDebts:
                column_number = 0
                for item in row:
                    sheet.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            # customer paids
            self.cr.execute(f'''SELECT id ,invoice,name ,phone ,paid ,allMoney,remain,date FROM debt''')
            debts = self.cr.fetchall()
            sheet = file.add_worksheet('دفعات العملاء  ')
            sheet.write(0, 0, "مسلسل")
            sheet.write(0, 1, "الفاتورة")
            sheet.write(0, 2, "الاسم")
            sheet.write(0, 3, "الهاتف")
            sheet.write(0, 4, "المدفوع")
            sheet.write(0, 5, "الإجمالى")
            sheet.write(0, 6, "المتبقى")
            sheet.write(0, 7, "التاريخ")
            row_number = 1
            for row in debts:
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
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    ExportAll()
