class Product:

    def __init__(self, name, tag, description, price, photo, composition) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.tag = tag
        self.photo = photo
        self.composition = composition
    

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


