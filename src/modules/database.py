import datetime
import sqlite3
from typing import List, Any

# for work when bot running
from modules.user import User
from modules.product import Product
from modules.order import Order

database_path = 'data/database.db'


# for testing database
"""from user import User
from product import Product
from order import Order

database_path = '../../data/database.db'"""


class Database:
    def __init__(self):
        pass

    def create_tables(self) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # --- создаём таблицу с меню ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Products (
            name TEXT NOT NULL PRIMARY KEY,
            description TEXT NOT NULL,
            price INTEGER
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL
            );
        """)

        # --- создаём таблицу с покупками ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
            date TEXT NOT NULL PRIMARY KEY,
            product TEXT NOT NULL,
            customer_id INTEGER,
            barman_id INTEGER,
            status TEXT NOT NULL,
            FOREIGN KEY (product) REFERENCES products(product),
            FOREIGN KEY (customer_id) REFERENCES user_base(id),
            FOREIGN KEY (barman_id) REFERENCES user_base(id)
            );
         """)
        conn.commit()
        conn.close()

    def insert_order(self, order: Order) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO orders (date, product, customer_id, barman_id, status) 
            VALUES (?, ?, ?, ?, ?)""",
                    (order.date, order.product, order.customer_id, order.barman_id, order.status))
        conn.commit()
        conn.close()

    def insert_product(self, product: Product) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO products (name, description, price)
            values (?, ?, ?)""",
                    (product.name, product.description, product.price)
                    )
        conn.commit()
        conn.close()

    def insert_user(self, user: User) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO  Users values (?, ?, ?)""",
                    (user.id, user.name, user.type)
                    )
        conn.commit()
        conn.close()

    def delete_order(self, order: Order) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Orders WHERE date = ?', (order.date,))
        conn.commit()
        conn.close()

    def delete_user(self, user: User) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Users WHERE id = ?', (user.id,))
        conn.commit()
        conn.close()

    def delete_product(self, product: Product) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Products WHERE name = ?', (product.name,))
        conn.commit()
        conn.close()

    def get_all_products(self):
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products')
        rows: list = cur.fetchall()
        conn.close()
        if rows is None:
            return None
        # Конвертирование в список Products
        result: list[Product] = []
        for row in rows:
            result.append(Product(row[0], row[1], row[2]))

        return result

    def get_all_users(self):
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users')
        rows: list = cur.fetchall()
        conn.close()
        if rows is None:
            return None
        # Конвертирование в список Products
        result: list[User] = []
        for row in rows:
            result.append(User(row[0], row[1], row[2]))

        return result

    def get_all_orders(self):
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Orders')
        rows: list = cur.fetchall()
        conn.close()
        if rows is None:
            return None
        # Конвертирование в список Products
        result: list[Order] = []
        for row in rows:
            result.append(Order(row[0], row[1], row[2], row[3], row[4]))

        return result

    def get_user_by_id(self, user_id: int) -> User:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
        found = cur.fetchone()
        conn.close()
        if found is None:
            return None
        return User(found[0], found[1], found[2])


    def get_product_by_name(self, name: str) -> Product:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products WHERE name = ?', (name,))
        found = cur.fetchone()
        if found is None:
            return None
        conn.close()
        return Product(found[0], found[1], found[2])


    def get_order_by_date(self, order_date: str) -> Order:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE date = ?", (order_date,))
        found = cur.fetchone()
        conn.close()
        return Order(found[0], found[1], found[2], found[3], found[4])


    def get_orders_by_customer_id(self, id: int):
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE customer_id = ?", (id,))
        rows: list = cur.fetchall()
        conn.close()
        if rows is None:
            return None
        # Конвертирование в список Products
        result: list[Order] = []
        for row in rows:
            result.append(Order(row[0], row[1], row[2], row[3], row[4]))
        return result

    def get_orders_queue(self):
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE status = ?", ("размещён",))
        rows: list = cur.fetchall()
        conn.close()
        if rows is None:
            return None
        # Конвертирование в список Products
        result: list[Order] = []
        for row in rows:
            result.append(Order(row[0], row[1], row[2], row[3], row[4]))
        return result

    def update_order(self, order: Order):
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            UPDATE orders SET barman_id = ?, status = ? WHERE date = ?""", (order.barman_id, order.status, order.date,))
        conn.commit()
        conn.close()


"""    def get_product_by_name(self, name) -> Product:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products WHERE name = ?', (name))
        found_product = cur.fetchone()
        conn.close()

        return Product(found_product[0], found_product[1], found_product[2])"""  # Пока не требуется (и пока не работает)

"""    def find_in_table_by_value_in_row(self, table_name, column_title, value) -> object:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM ? WHERE ? = ?', (table_name, column_title, value))
        found = cur.fetchone()
        conn.close()
        return found"""  # Не работают ? в SQLе (Наверное и не понадобится)

# tests area
"""order = Order("qdqd", "Шот", 234124, 133, 'placed')
db = Database()
db.create_tables()
db.insert_order(order)"""