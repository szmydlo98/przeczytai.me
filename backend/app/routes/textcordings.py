from fastapi import APIRouter, Depends, Query, Response, status

from app.auth import CurrentUser, get_current_user
from app.config import Settings, get_settings
from app.errors import ApiException
from app.models import TextCording, TextCordingCreateRequest, TextCordingListResponse
from app.repositories.textcordings import ProcessingStartError, TextCordingRepository

router = APIRouter(prefix="/api/v1/textcordings", tags=["textcordings"])


def get_textcording_repository(settings: Settings = Depends(get_settings)) -> TextCordingRepository:
    return TextCordingRepository(settings.textcordings_table_name, settings.processor_function_name)


def _textcording(item: dict) -> TextCording:
    return TextCording(
        id=item["textcording_id"],
        original_text=item["original_text"],
        read_text=item.get("read_text"),
        recording=item.get("recording"),
        vendor=item.get("vendor"),
        voice=item.get("voice"),
        status=item["status"],
        metadata=item.get("metadata", {}),
        char_count=int(item["char_count"]),
        created_at=item["created_at"],
        updated_at=item["updated_at"],
    )


@router.post("", response_model=TextCording, status_code=status.HTTP_201_CREATED)
async def create_textcording(
    request: TextCordingCreateRequest,
    user: CurrentUser = Depends(get_current_user),
    repo: TextCordingRepository = Depends(get_textcording_repository),
    settings: Settings = Depends(get_settings),
) -> TextCording:
    original_text = request.original_text.strip()
    if not original_text:
        raise ApiException("validation_error", "Original text must not be empty", 422)
    if len(original_text) > settings.max_text_chars:
        raise ApiException("payload_too_large", "Original text is too large", 413)
    try:
        item = repo.create(user.user_id, original_text, request.vendor, request.voice)
    except ProcessingStartError as exc:
        raise ApiException(
            "processing_start_failed",
            "Failed to start textcording processing",
            500,
        ) from exc
    return _textcording(item)


@router.get("", response_model=TextCordingListResponse)
async def list_textcordings(
    user: CurrentUser = Depends(get_current_user),
    repo: TextCordingRepository = Depends(get_textcording_repository),
    limit: int = Query(default=20, ge=1, le=50),
    cursor: str | None = None,
) -> TextCordingListResponse:
    items, next_cursor = repo.list(user.user_id, limit, cursor)
    return TextCordingListResponse(
        items=[_textcording(item) for item in items],
        next_cursor=next_cursor,
    )


@router.get("/{textcording_id}", response_model=TextCording)
async def get_textcording(
    textcording_id: str,
    user: CurrentUser = Depends(get_current_user),
    repo: TextCordingRepository = Depends(get_textcording_repository),
) -> TextCording:
    item = repo.get(user.user_id, textcording_id)
    if not item:
        raise ApiException("not_found", "TextCording not found", 404)
    return _textcording(item)


@router.delete("/{textcording_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_textcording(
    textcording_id: str,
    user: CurrentUser = Depends(get_current_user),
    repo: TextCordingRepository = Depends(get_textcording_repository),
) -> Response:
    repo.delete(user.user_id, textcording_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
