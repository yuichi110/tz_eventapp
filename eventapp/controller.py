from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from eventapp.service import EventService, ImageService
from eventapp.model import EventSchema


class Router(APIRouter):
    def __init__(
        self,
        event_service: EventService,
        image_service: ImageService,
    ):
        super().__init__()
        self._event_service = event_service
        self._image_service = image_service

        self.add_api_route(
            "/api/event/categories/",
            self.get_categories,
            methods=["GET"],
            response_model=list[str],
        )

        self.add_api_route(
            "/api/event/all-categories/",
            self.get_all_category_events,
            methods=["GET"],
            response_model=list[EventSchema],
        )

        self.add_api_route(
            "/api/event/categories/{category}/",
            self.get_category_events,
            methods=["GET"],
            response_model=list[EventSchema],
        )

        self.add_api_route(
            "/api/event/categories/{category}/{event_uuid}",
            self.get_category_event,
            methods=["GET"],
            response_model=EventSchema,
        )

        self.add_api_route(
            "/image/event/{image_uuid}",
            self.get_image,
            methods=["GET"],
        )

    def get_categories(self):
        return self._event_service.get_event_categories()

    def get_all_category_events(self):
        return self._event_service.get_all_category_events()

    def get_category_events(self, category: str):
        return self._event_service.get_category_events(category)

    def get_category_event(self, category: str, event_uuid: str):
        return self._event_service.get_event(event_uuid)

    def get_image(self, name: str):
        data, media_type = self._image_service.get(name)
        return StreamingResponse(data, media_type=media_type)
