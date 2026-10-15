from src.app.api.v1.users.user_router import UserRouter
from src.app.core.utils.error_handler import ErrorHandler
from src.app.schemas.users.emailloginreq import EmailLoginReq


def include_route(routerobj: UserRouter) -> None:
    @routerobj.router.post("/email-login")
    async def login(user: EmailLoginReq):
        try:
            # check if user exists in db, remember its an async function
            user = await routerobj.user_service.find_user_by_email(user.email)
            return ErrorHandler.handle_success(
                data={"user": user},
                message="user login successful"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)


