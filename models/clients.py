from datetime import date


class Client:
    """Class for client"""

    def __init__(self) -> None:
        """
        commercial_id: user_id
        """
        self.id = int()
        self.name = str()
        self.email = str()
        self.phone = str()
        self.first_contact = date()
        self.last_contact = date()
        self.company_id = int()
        self.commercial_id = int()
