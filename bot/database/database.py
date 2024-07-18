"""Database module."""

import sqlite3

from bot.database.user import User
from bot.database.product import Product
from bot.database.order import Order


class Database:
    """Database class."""

    def __init__(self, database_file_name="database.db"):
        database_folder = "data/"
        database_path = database_folder + database_file_name
        self.database_file_name = database_file_name
        self.database_path = database_path
        self.database_folder = database_folder

    def create_tables(self) -> None:
        """Creates database tables."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()

        # --- создаём таблицу с меню ---
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Products (
            name TEXT NOT NULL PRIMARY KEY,
            description TEXT NOT NULL,
            price INTEGER
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL
            );
        """
        )

        # --- создаём таблицу с покупками ---
        cur.execute(
            """
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
         """
        )
        conn.commit()
        conn.close()

    def insert_order(self, order: Order) -> None:
        """Insert order into the database."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO orders (date, product, customer_id, barman_id, status)
            VALUES (?, ?, ?, ?, ?)""",
            (
                order.date,
                order.product,
                order.customer_id,
                order.barman_id,
                order.status,
            ),
        )
        conn.commit()
        conn.close()

    def insert_product(self, product: Product) -> None:
        """Insert product into the database."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO products (name, description, price)
            values (?, ?, ?)""",
            (product.name, product.description, product.price),
        )
        conn.commit()
        conn.close()

    def insert_user(self, user: User) -> None:
        """Insert user into the database."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO  Users values (?, ?, ?)""",
            (user.id, user.name, user.type),
        )
        conn.commit()
        conn.close()

    def delete_order(self, order: Order) -> None:
        """Delete order from the database."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM Orders WHERE date = ?", (order.date,))
        conn.commit()
        conn.close()

    def delete_user(self, user: User) -> None:
        """Delete user from the database."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE id = ?", (user.id,))
        conn.commit()
        conn.close()

    def delete_product(self, product: Product) -> None:
        """Delete product from the database"""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM Products WHERE name = ?", (product.name,))
        conn.commit()
        conn.close()

    def get_all_products(self):
        """Returns all products from the database to list."""
        # Получение списка списков из бд
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products")
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
        """Returns all users from the database to list."""
        # Получение списка списков из бд
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")
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
        """Returns all orders from the database to list."""
        # Получение списка списков из бд
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders")
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
        """Returns a user from the database if user with user_id exists."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
        found = cur.fetchone()
        conn.close()
        if found is None:
            return None
        return User(found[0], found[1], found[2])

    def get_product_by_name(self, name: str) -> Product:
        """Returns a product if product with name exists."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Products WHERE name = ?", (name,))
        found = cur.fetchone()
        if found is None:
            return None
        conn.close()
        return Product(found[0], found[1], found[2])

    def get_order_by_date(self, order_date: str) -> Order:
        """Returns a order if order with order_date exists."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE date = ?", (order_date,))
        found = cur.fetchone()
        conn.close()
        return Order(found[0], found[1], found[2], found[3], found[4])

    def get_orders_by_customer_id(self, customer_id: int):
        """Returns a list of orders if user with customer_id exists."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Orders WHERE customer_id = ?", (customer_id,))
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
        """Returns a list of orders which status is размещён."""
        conn = sqlite3.connect(self.database_path)
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
        """Updates the order info."""
        conn = sqlite3.connect(self.database_path)
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE orders SET barman_id = ?, status = ? WHERE date = ?""",
            (
                order.barman_id,
                order.status,
                order.date,
            ),
        )
        conn.commit()
        conn.close()
