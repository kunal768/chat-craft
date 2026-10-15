from src.app.crud.user.repo import Repository
from src.app.models.user import User 
from src.app.models.userdocs import UserDocs
from src.app.models.apikeys import ApiKeys
from src.app.crud.apikeys.service import ApiKeysService
from src.app.crud.docs.service import DocsService
from src.app.core.utils.errors import (
    CustomException,
    UserNotFoundError,
    EmailAlreadyExistsError,
    InvalidEmailError
)

class UserService:
    """
    Service layer for user-related operations.
    Handles user CRUD operations and business logic.
    """
    
    def __init__(
        self, 
        repo: Repository, 
        api_keys_service: ApiKeysService, 
        docs_service: DocsService
    ):
        """
        Initialize UserService with required dependencies.
        
        Args:
            repo: Repository for user data access
            api_keys_service: Service for API key operations
            docs_service: Service for document operations
        """
        self.repo = repo 
        self.api_keys_service = api_keys_service
        self.docs_service = docs_service

    async def create_user(self, user: User) -> User:
        """
        Create a new user and initialize associated resources.
        
        Args:
            user: User object containing user data
            
        Returns:
            Created user object
            
        Raises:
            InvalidEmailError: If email is missing or invalid
            EmailAlreadyExistsError: If user with email already exists
        """
        try:
            # Validate input
            if not user or not user.email:
                raise InvalidEmailError("Email is required")
            
            # Check if user already exists
            existing_user = await self.repo.get_user_by_email(user.email)
            if existing_user:
                raise EmailAlreadyExistsError(f"User with email {user.email} already exists")

            # Create user
            created_user_id = await self.repo.create_user(user)
            if isinstance(created_user_id, Exception):
                raise EmailAlreadyExistsError()
            
            try:
                # Initialize user resources
                await self._initialize_user_resources(created_user_id=created_user_id)
            except Exception as e:
                # If resource initialization fails, we should clean up the created user
                await self.repo.delete_user(str(created_user_id))
                raise e

            
            return user     
        
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise EmailAlreadyExistsError(str(e))

    async def find_user_by_email(self, email: str) -> User:
        """
        Find a user by their email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User object if found
            
        Raises:
            InvalidEmailError: If email is missing or invalid
            UserNotFoundError: If user not found
        """
        try:
            if not email:
                raise InvalidEmailError("Email is required")
                
            res = await self.repo.get_user_by_email(email)
            if not res or isinstance(res, Exception):
                raise UserNotFoundError(f"User with email {email} not found")
            return User.model_validate(res)
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise UserNotFoundError(str(e))
        
    async def find_user_by_id(self, user_id: str) -> User:
        """
        Find a user by their ID.
        
        Args:
            user_id: User ID to search for
            
        Returns:
            User object if found
            
        Raises:
            UserNotFoundError: If user not found or ID is invalid
        """
        try:
            if not user_id:
                raise UserNotFoundError("User ID is required")
                
            user = await self.repo.get_user_by_id(user_id)
            if not user or isinstance(user, Exception):
                raise UserNotFoundError(f"User with ID {user_id} not found")
            return User.model_validate(user)
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise UserNotFoundError(str(e))

    async def _initialize_user_resources(self, created_user_id: str  | None) -> None:
        """
        Initialize resources for a new user.

        Args:
            created_user_id: ID of the user to initialize resources for

        Raises:
            Exception: If resource initialization fails
        """
        # Initialize user API keys
        # api_keys_obj = ApiKeys(user_id=str(created_user_id))  # Pass explicit user ID
        # await self.api_keys_service.create_api_key(api_key=api_keys_obj)

        # # Initialize user docs (optional)
        user_docs = UserDocs(user_id=str(created_user_id))
        await self.docs_service.create_userdoc(user_docs)
