import sqlite3
from typing import List, Any

from user import User
from product import Product
from order import Order

database_path = '../../data/database.db'


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

    def insert_order(self, date, product, customer_id, barman_id, status) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO orders (date, product, customer_id, barman_id, status) 
            VALUES (?, ?, ?, ?, ?, ?)""",
                    (date, product, customer_id, barman_id, status))
        conn.commit()
        conn.close()

    def insert_product(self, product) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO products (name, description, price)
            values (?, ?, ?)""",
                    (product.name, product.description, product.price)
                    )
        conn.commit()
        conn.close()

    def insert_user(self, user) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO  Users values (?, ?, ?)""",
                    (user.id, user.name, user.type)
                    )
        conn.commit()
        conn.close()

    def delete_order(self, order) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Orders WHERE date = ?', (order.date,))
        conn.commit()
        conn.close()

    def delete_user(self, user) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Users WHERE id = ?', (user.id,))
        conn.commit()
        conn.close()

    def delete_product(self, product) -> None:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM Products WHERE name = ?', (product.name,))
        conn.commit()
        conn.close()


""" def get_products(self) -> list | Product:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products')
        rows: list = cur.fetchall()
        conn.close()
        return rows""" # Пока не работает, как считывать данные в объект, вопрос хороший, походу там надо повеселиться)

""" def get_product_by_name(self, product) -> Product:
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM Products WHERE name = ?', (product.name,))
        return"""  # Это пока не надо
