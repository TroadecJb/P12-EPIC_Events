from datetime import date


class Contract:
    """Class for contract"""

    def __init__(self) -> None:
        """
        commercial_id: user_id
        """
        self.id = int()
        self.client_id = int()
        self.date_creation = date()
        self.cost_total = float()
        self.cost_remaining = float()
        self.valid = bool()
        self.commercial_id = int()
