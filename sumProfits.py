from encrypted import Connection


class Profits(Connection):
    def __init__(self):
        self.secondDate = None
        self.db = None
        self.firstDate = None
        self.connector()

    def all_profit(self):
        all_profit = 0
        try:
            self.cr.execute('SELECT profit FROM daily_sales ')
            profits = self.cr.fetchall()
            for profit in profits:
                all_profit = all_profit + profit[0]
            return '{:.0f}'.format(all_profit)
        except Exception as e:
            print(str(e), 'Profits.all_profit()')
            return "0"

    def filterProfit(self, firstDate, secondDate):
        self.firstDate = firstDate
        self.secondDate = secondDate
        all_profits = 0
        try:
            self.cr.execute(f'SELECT profit FROM daily_sales WHERE date between "{self.firstDate}" AND "{self.secondDate}"  ')
            profits = self.cr.fetchall()
            for profit in profits:
                all_profits = all_profits + int(profit[0])
            print(type(all_profits))
            print(all_profits)
            return str(all_profits)
        except :
            return "0"

