# import MySQLdb
from PyQt5.QtWidgets import *
from mysql.connector import connect


class ExportBackUp:

    def __init__(self) :
        print('export sql')

    def export_sql(self, path):
        self.path = path
        try:
            con = connect(host='localhost', user='root', passwd='', db='sports')
            cur = con.cursor()

            cur.execute("SHOW TABLES")
            data = ""
            tables = []
            for table in cur.fetchall():
                tables.append(table[0])

            for table in tables:
                data += "DROP TABLE IF EXISTS `" + str(table) + "`;"

                cur.execute("SHOW CREATE TABLE `" + str(table) + "`;")
                data += "\n" + str(cur.fetchone()[1]) + ";\n\n"

                cur.execute("SELECT * FROM `" + str(table) + "`;")
                for row in cur.fetchall():
                    data += "INSERT INTO `" + str(table) + "` VALUES("
                    first = True
                    for field in row:
                        if not first:
                            data += ', '
                        data += '"' + str(field) + '"'
                        first = False


                    data += ");\n"
                data += "\n\n"
        
            filename =f"{self.path}/sports.sql"
            filename_2 = 'sports.sql'

            FILE = open(filename,"w", encoding='UTF-8')
            FILE.writelines(data)
            FILE.close()
        # export to current directory
            FILE2 = open(filename_2,"w", encoding='UTF-8')
            FILE2.writelines(data)
            FILE2.close()


        except Exception as e:
            print(e)