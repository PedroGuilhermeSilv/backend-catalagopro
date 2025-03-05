class Error(Exception):
    def __init__(self):
        self.msg = ""
        self.status_code = 500

    def __str__(self):
        return self.msg


class InvalidSlugError(Error):
    def __init__(self):
        self.msg = "Invalid slug"
        self.status_code = 422
