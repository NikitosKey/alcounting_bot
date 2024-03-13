import datetime
from product import Product


class Order:

    def __init__(self, id, customer_id, choice, date, status, barman_id) -> None:
        self.id = id
        self.customer_id = customer_id
        self.choice = choice
        self.date = date
        self.status = status
        self.barman_id = barman_id        

    
    def get_id(self) -> int:
        return self.id


    def get_customer_id(self) -> str:
        return self.customer_id


    def get_choice(self) -> Product:
        return self.choice
    

    def get_date(self) -> datetime:
        return self.date
    

    def get_status(self) -> str:
        return self.status


    def get_barman_id(self) -> str:
        return self.barman_id
        

    def set_id(self, val) -> None:
        self.id = val
    
    
    def set_customer_id(self, val) -> None:
        self.customer_id = val


    def get_choice(self, val) -> None:
        self.choice = val 


    def set_date(self, val) -> None:
        self.date = val


    def set_status(self, val) -> None:
        self.status = val


    def set_barman_id(self, val) -> None:
        self.barman_id = val