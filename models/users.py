class User:
    """Abstractclass for user"""

    def __init__(self) -> None:
        self.id = int()
        self.name = str()
        self.email = str()
        self.phone = str()
        self.role_id = int()

    def user_test(self):
        print("i'm user")

    def change_password(self):
        pass

    def client_read(self):
        pass

    def contract_read(self):
        pass

    def event_read(self):
        pass

    def company_read(self):
        pass

    def address_read(self):
        pass

    def address_create(self):
        pass

    def address_update(self):
        pass
