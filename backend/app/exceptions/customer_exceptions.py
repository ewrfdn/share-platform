class BadRequestException(Exception):
    """Exception raised for bad requests"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class NotFoundException(Exception):
    """Exception raised for not found errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
