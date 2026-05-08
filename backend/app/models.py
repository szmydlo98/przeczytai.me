from pydantic import BaseModel, Field


class ApiError(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ApiError


class TextCordingCreateRequest(BaseModel):
    original_text: str
    vendor: str | None = Field(default=None, max_length=120)
    voice: str | None = Field(default=None, max_length=120)


class TextCording(BaseModel):
    id: str
    original_text: str
    read_text: str | None = None
    recording: str | None = None
    vendor: str | None = None
    voice: str | None = None
    status: str
    metadata: dict[str, object] = Field(default_factory=dict)
    char_count: int
    created_at: str
    updated_at: str


class TextCordingListResponse(BaseModel):
    items: list[TextCording]
    next_cursor: str | None = None
