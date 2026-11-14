from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class VideoRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    mode: Literal["text_to_video", "image_to_video"] = "text_to_video"
    image_url: HttpUrl | None = None
    workflow: dict[str, Any] | None = None
    width: int = Field(default=432, ge=64, le=1920)
    height: int = Field(default=768, ge=64, le=1920)
    frames: int = Field(default=49, ge=1, le=1000)
    fps: int = Field(default=16, ge=1, le=60)


class VideoJob(BaseModel):
    id: str
    status: str
    output: dict[str, Any] | None = None
    error: str | None = None
