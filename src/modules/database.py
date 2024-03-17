import sqlite3
from typing import List, Any

from modules.user import User
from modules.product import Product
from modules.order import Order

database_path = 'data/database.db'


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
            date INTEGER PRIMARY KEY,
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
            INSERT OR IGNORE INTO orders (date, product, customer_id, barman_id, status) 
            VALUES (?, ?, ?, ?, ?, ?)""",
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

    def get_all_products(self) -> List[Product]:
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products')
        rows: list = cur.fetchall()
        conn.close()
        # Конвертирование в список Products
        result: list[Product] = []
        for row in rows:
            result.append(Product(row[0], row[1], row[2]))

        return result

    def get_all_users(self) -> List[User]:
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Users')
        rows: list = cur.fetchall()
        conn.close()
        # Конвертирование в список Products
        result: list[User] = []
        for row in rows:
            result.append(User(row[0], row[1], row[2]))

        return result

    def get_all_orders(self) -> List[Order]:
        # Получение списка списков из бд
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Orders')
        rows: list = cur.fetchall()
        conn.close()
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
        return User(found[0], found[1], found[2])


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
