class Profit:
    def __init__(self):
        print('profitModule')

    def profit(self, price, itemPrice, count):
        itemProfit = float(price) - float(itemPrice)
        totalProfit = itemProfit * float(count)
        return totalProfit

