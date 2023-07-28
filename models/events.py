from datetime import date


class Event:
    """Class for event"""

    def __init__(self) -> None:
        """
        support_id: user_id
        """
        self.id = int()
        self.contract_id = int()
        self.support_id = int()
        self.date_begin = date()
        self.date_end = date()
        self.address_id = int()
        self.number_attendee = int()
        self.note = str()
