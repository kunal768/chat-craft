from src.app.api.v1.users.user_router import UserRouter
from src.app.core.utils.error_handler import ErrorHandler


def include_route(routerobj: UserRouter) -> None:
    @routerobj.router.get("/id")
    async def get_user_by_id(user_id: str):
        try:
            user = await routerobj.user_service.find_user_by_id(user_id=user_id)
            return ErrorHandler.handle_success(
                data={"user": user},
                message="user found"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)
        