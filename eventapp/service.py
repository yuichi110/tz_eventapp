import io
import os
from eventapp.repository import (
    AbstractEventRepository,
    AbstractImageRepository,
)
from eventapp.model import EventSchema
from eventapp.exceptions import ClientException

IMAGE_MEDIA_DICT = {
    ".apng": "image/apng",
    ".avif": "image/avif",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".ico": "image/vnd.microsoft.icon",
    ".svg": "image/svg+xml",
}


class EventService:
    def __init__(self, event_repo: AbstractEventRepository):
        self._event_repo = event_repo

    def get_event_categories(self) -> list[str]:
        return self._event_repo.get_event_categories()

    def get_all_category_events(self) -> list[EventSchema]:
        return self._event_repo.get_all_category_events()

    def get_category_events(self, category: str) -> list[EventSchema]:
        return self._event_repo.get_category_events(category)

    def get_event(self, event_uuid: str) -> EventSchema:
        return self._event_repo.get_event(event_uuid)


class ImageService:
    def __init__(self, image_repo: AbstractImageRepository):
        self._image_repo = image_repo

    def get(self, file_name: str) -> tuple[io.BytesIO, str]:
        media_type = self._get_media_type(file_name)
        data = self._image_repo.get(file_name)
        return data, media_type

    def _get_media_type(self, file_name: str) -> str:
        ext = os.path.splitext(file_name)[1].lower()
        if ext not in IMAGE_MEDIA_DICT:
            raise ClientException("media type not supported")
        return IMAGE_MEDIA_DICT[ext]
