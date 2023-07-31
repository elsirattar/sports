from encrypted import Connection


class TotalCapitalModule(Connection):
    def __init__(self):
        self.connector()

    def total_capital(self):
        total_item_price = []
        try:
            self.cr.execute('SELECT itemCost, count FROM item ')
            items = self.cr.fetchall()
            for i in items:
                totalCapital = i[0] * i[1]
                total_item_price.append(round(totalCapital, 1))
            print(total_item_price)
            totCapital_ = sum(total_item_price)
            return '{:.1f}'.format(totCapital_)
        except:
            return "0"

