import datetime
from modules.product import Product


class Order:

    def __init__(self, date, product, customer_id, barman_id, status) -> None:
        """self.id = id"""
        self.date = date
        self.product = product
        self.customer_id = customer_id
        self.barman_id = barman_id
        self.status = status

    """def get_order_id(self) -> int:
        return self.id"""

    def get_order_customer_id(self) -> str:
        return self.customer_id

    def get_order_product(self) -> Product:
        return self.choice

    def get_order_date(self) -> datetime:
        return self.date

    def get_order_status(self) -> str:
        return self.status

    def get_order_barman_id(self) -> str:
        return self.barman_id

    """def set_order_id(self, val) -> None:
        self.id = val"""

    def set_order_customer_id(self, val) -> None:
        self.customer_id = val

    def get_order_product(self, val) -> None:
        self.product = val

    def set_order_date(self, val) -> None:
        self.date = val

    def set_order_status(self, val) -> None:
        self.status = val

    def set_order_barman_id(self, val) -> None:
        self.barman_id = val
