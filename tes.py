# import MySQLdb
# import os
# import datetime

# con = MySQLdb.connect(host='localhost', user='root', passwd='', db='special_awg')
# cur = con.cursor()

# cur.execute("SHOW TABLES")
# data = ""
# tables = []
# for table in cur.fetchall():
#     tables.append(table[0])

# for table in tables:
#     data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

#     cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
#     data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

#     cur.execute("SELECT * FROM `" + str(table) + "`;")
#     for row in cur.fetchall():
#         data += "INSERT INTO `" + str(table) + "` VALUES("
#         first = True
#         for field in row:
#             if not first:
#                 data += ', '
#             data += '"' + str(field) + '"'
#             first = False


#         data += ");\n"
#     data += "\n\n"

# now = datetime.datetime.now()
# filename = "database.sql"

# FILE = open(filename,"w")
# FILE.writelines(data)
# FILE.close()
# from datetime import date ,timedelta

# print(date.today() + timedelta(days = 30))

from datetime import *

# today = date.today().strftime("%Y:%m:%d")
# print(today)
# input_dt =datetime(int(today[:4]), int(today[5:7]), int(today[8:]))
# print("The original date is:", input_dt)

# next_month = input_dt.replace(day=28) + timedelta(days=4)
# res = next_month - timedelta(days=next_month.day)
# print(f"Last date of month is:", res.date())

try:
  datetime.strptime("2022-02-25", '%Y-%m-%d')
  print("==> Correct date string")
except ValueError:
  print("Incorrect date string")