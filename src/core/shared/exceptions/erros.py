class Error(Exception):
    def __init__(self):
        self.msg = ""
        self.status_code = 500

    def __str__(self):
        return self.msg


class InvalidEmailError(Error):
    def __init__(self):
        self.msg = "Invalid email"
        self.status_code = 400


class InvalidPasswordError(Error):
    def __init__(self):
        self.msg = "Password must be at least 8 characters long"
        self.status_code = 403


class InvalidUserError(Error):
    def __init__(self):
        self.msg = "Invalid user"
        self.status_code = 403


class UserNotFoundError(Error):
    def __init__(self):
        self.msg = "User not found"
        self.status_code = 403
