class Product:

    def __init__(self, name, description, price) -> None:
        # self.tag = tag
        self.name = name
        # self.photo = photo
        self.description = description
        self.price = price
        # self.composition = composition

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_description(self) -> str:
        return self.description

    def set_name(self, val) -> None:
        self.name = val

    def set_price(self, val) -> None:
        self.price = val

    def set_description(self, val) -> None:
        self.description = val
