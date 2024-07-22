"""Database module init."""

__all__ = ["Database", "Order", "Product", "User"]

from bot.database.order import Order
from bot.database.product import Product
from bot.database.user import User
from bot.database.database import Database
