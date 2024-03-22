class User:

    def __init__(self, id, name, type) -> None:
        self.id = id
        self.name = name
        self.type = type

        if self.type not in ['barman', 'admin', 'customer']:
            raise ValueError("Invalid user type")

    def get_user_name(self) -> str:
        return self.name

    def get_user_id(self) -> str:
        return self.id

    def get_user_type(self) -> str:
        return self.type

    def set_user_name(self, name) -> None:
        self.name = name

    def set_user_id(self, user_id) -> None:
        self.id = user_id

    def set_user_type(self, user_type) -> None:
        self.type = user_type
