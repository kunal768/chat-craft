from src.app.api.v1.users.user_router import UserRouter 
from src.app.schemas.users.signupreq import SignUpReq
from src.app.core.utils.error_handler import ErrorHandler
from src.app.models.user import User
from src.app.schemas.std_response import StdResponse


def include_route(routerobj: UserRouter) -> None:
    @routerobj.router.post("/signup")
    async def signup(req : SignUpReq):
        try:
            user = await routerobj.user_service.create_user(user = User(email=req.email, name=req.name))
            return ErrorHandler.handle_success(
                data={"user": user},
                message="user creation successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)



    