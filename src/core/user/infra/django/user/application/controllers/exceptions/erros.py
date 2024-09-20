class InvalidEmail(ValueError):
    def __init__(self):
        super().__init__("You have not specified a valid e-mail address")
