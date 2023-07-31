import sqlite3


def count_profit():
    db = sqlite3.connect('businessdata.db')
    cr = db.cursor()

    cr.execute(f'SELECT item_name,price,count ,id ,date FROM daily_sales')
    data = cr.fetchall()
    total_profit = []
    for d in data:
        cr.execute(f'SELECT item_price FROM item WHERE name = "{d[0]}"')
        price = cr.fetchall()
        for p in price:
            profit = d[1] - p[0]

            tot_profit = profit * d[2]
            total_profit.append(tot_profit)

            cr.execute(f'UPDATE OR REPLACE daily_sales SET profit="{tot_profit}" WHERE id ="{d[3]}" ')
            db.commit()
