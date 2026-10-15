from fastapi import Depends, APIRouter
from src.app.api.v1.base_router import BaseRouter
from src.app.crud.user.service import UserService
from src.app.core.utils.singleton import Singleton


class UserRouter(BaseRouter, metaclass = Singleton):
    def __init__(self, user_service: UserService = Depends(UserService)):
        super().__init__(
            prefix="/v1/users",
            tags=["users"]
        )
        self.user_service = user_service
    
    def include_user_routes(self) -> APIRouter:
        from src.app.api.v1.users import signup, login, getuserbyid

        signup.include_route(self)
        login.include_route(self)
        getuserbyid.include_route(self)

        return self.router







