class User:

    def __init__(self, user_name, user_id, user_type):
        self.user_name = user_name
        self.user_id = user_id
        self.user_type = user_type

        if self.user_type not in ['barmen', 'admin', 'customer']:
            raise ValueError("Invalid user type")

    def get_user_name(self) -> str:
        return self.user_name

    def get_user_id(self) -> str:
        return self.user_id

    def get_user_type(self):
        return self.user_type

    def set_user_name(self, name):
        self.user_name = name

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_user_type(self, user_type):
        self.user_type = user_type
