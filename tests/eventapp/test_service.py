import os
from pathlib import Path
from eventapp.repository import MockEventRepository, LocalImageRepository
from eventapp.service import EventService, ImageService


def test_event_service():
    service = EventService(MockEventRepository())
    assert len(service.get_event_categories()) == 4
    assert len(service.get_all_category_events()) == 10
    assert len(service.get_category_events("horce-race")) == 4
    service.get_event("8c1ce714-0c12-4660-861e-dc0dc14e60a7")


def test_image_repo():
    image_dir_path = os.path.join(
        Path(__file__).parent.parent.parent,
        "eventapp",
        "assets",
        "images",
    )

    repo = LocalImageRepository(image_dir_path)
    service = ImageService(repo)
    service.get("8ec594e0-689a-4b99-b80a-8abf1757befd.png")
