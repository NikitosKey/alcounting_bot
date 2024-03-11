import sqlite3 as sl

con = sl.connect('../../data/database.db')

with con:
    # получаем количество таблиц с нужным нам именем
    data = con.execute("select count(*) from sqlite_master where type='table' and name='goods'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для товаров
            with con:
                con.execute("""
                    CREATE TABLE user_base (
                        id VARCHAR(20) PRIMARY KEY,
                        name INTEGER,
                        type INTEGER
                    );
                """)

# подготавливаем множественный запрос
sql = 'INSERT INTO goods (product, count, price) values(?, ?, ?)'
# указываем данные для запроса
data = [
    ('стол', 2, 3000),
    ('стул', 5, 1000),
    ('табурет', 1, 500)
]

# --- создаём таблицу с покупками ---
# открываем базу
with con:
    # получаем количество таблиц с нужным нам именем — orders
    data = con.execute("select count(*) from sqlite_master where type='table' and name='orders'")
    for row in data:
        # если таких таблиц нет
        if row[0] == 0:
            # создаём таблицу для покупок
            with con:
                con.execute("""
                    CREATE TABLE orders (
                        order_id INTEGER PRIMARY KEY,
                        product VARCHAR,
                        amount INTEGER,
                        client_id INTEGER,
                        FOREIGN KEY (product) REFERENCES goods(product),
                        FOREIGN KEY (client_id) REFERENCES clients(id)
                    );
                """)
