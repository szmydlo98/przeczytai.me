from fastapi import Depends, Request

from app.config import Settings, get_settings
from app.errors import ApiException


class CurrentUser:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id


async def get_current_user(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    event = request.scope.get("aws.event") or {}
    claims = (
        event.get("requestContext", {})
        .get("authorizer", {})
        .get("jwt", {})
        .get("claims", {})
    )
    user_id = claims.get("sub")
    if isinstance(user_id, str) and user_id:
        return CurrentUser(user_id)
    if settings.auth_required:
        raise ApiException("unauthorized", "Missing API Gateway JWT claims", 401)
    return CurrentUser(settings.unauthenticated_user_id)
