from fastapi import Request

from app.errors import ApiException


class CurrentUser:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


async def get_current_user(request: Request) -> CurrentUser:
    event = request.scope.get("aws.event") or {}
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )
    user_id = claims.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise ApiException("unauthorized", "Missing API Gateway JWT claims", 401)
    return CurrentUser(user_id)
