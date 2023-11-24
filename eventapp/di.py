import os
from pathlib import Path
from eventapp.service import EventService, ImageService
from eventapp.repository import MockEventRepository, LocalImageRepository


class DiContainer:
    def __init__(self):
        # build up to services.
        # not controller. For avoiding dependance to web frameworks
        ...

    def get_services(
        self,
    ) -> tuple[EventService, ImageService]:
        event_service = self._get_event_service()
        image_service = self._get_image_service()
        return event_service, image_service

    def _get_event_service(self) -> EventService:
        return EventService(MockEventRepository())

    def _get_image_service(self) -> ImageService:
        image_dir_path = os.path.join(Path(__file__).parent, "assets", "images")
        return ImageService(LocalImageRepository(image_dir_path))
