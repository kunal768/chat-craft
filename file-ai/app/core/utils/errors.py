from app.core.utils.status_codes import StatusCodes

class CustomException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        

""" add custom exceptions below """

class UserNotFoundError(CustomException):
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=StatusCodes.NOT_FOUND)
        

        
class InvalidCredentialsError(CustomException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=StatusCodes.UNAUTHORIZED)
        
        
        
class EmailAlreadyExistsError(CustomException):
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)
        
        
        
class InvalidEmailError(CustomException):
    def __init__(self, message: str = "Invalid email"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)
        
        
class InvalidApiKeyError(CustomException):
    def __init__(self, message: str = "Invalid API key"):
        super().__init__(message, status_code=StatusCodes.UNAUTHORIZED)
        

""" document errors """
class DocumentNotFoundError(CustomException):
    def __init__(self, message: str = "Document not found"):
        super().__init__(message, status_code=StatusCodes.NOT_FOUND)


class DocumentCreationError(CustomException):
    def __init__(self, message: str = "Failed to create document"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)


class DocumentUpdateError(CustomException):
    def __init__(self, message: str = "Failed to update document"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)


class DocumentDeletionError(CustomException):
    def __init__(self, message: str = "Failed to delete document"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)


class InvalidDocumentDataError(CustomException):
    def __init__(self, message: str = "Invalid document data"):
        super().__init__(message, status_code=StatusCodes.BAD_REQUEST)
        
        
        