class NameIsRequired(Exception):
    def __init__(self):
        self.message = 'Name is required'
        super().__init__(self.message)

class NameShouldBeLessThan150Characters(Exception):
    def __init__(self):
        self.message = 'Name should be less than 150 characters'
        super().__init__(self.message)

class IdIsRequired(Exception):
    def __init__(self):
        self.message = 'Id is required'
        super().__init__(self.message)

class NameShouldBeString(Exception):
    def __init__(self):
        self.message = 'Name should be string'
        super().__init__(self.message)
class IdShouldBeUUID(Exception):
    def __init__(self):
        self.message = 'Id should be uuid'
        super().__init__(self.message)