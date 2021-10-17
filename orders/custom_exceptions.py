class DatabaseInitException(Exception):
    """ Exception raised when MongoDB is unable to initialize the collections

    Attributes:
        message -- explaination of the exception
    """

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        exception_message = super().__str__()
        return f"User Error Message: {self.message}. System Error Message: {exception_message}"
