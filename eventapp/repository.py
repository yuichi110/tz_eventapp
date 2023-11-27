from abc import ABC, abstractmethod
import io
import os

import pandas as pd
from eventapp.model import EventSchema
from eventapp.exceptions import ClientException

_EVENT_CATEGORIES = ["horce-race", "boat-race", "bike-race", "auto-race"]

_EVENTS = [
    EventSchema(
        category="auto-race",
        id="17ca575f-cb16-42b3-b6ca-8945a1b105a3",
        name="第10レース結果",
        description="1番は田中。2番は山田",
        image_url="/images/event/8ec594e0-689a-4b99-b80a-8abf1757befd.png",
        date="",
    ),
    EventSchema(
        category="horce-race",
        id="51cfd0d3-d513-4d3e-9912-eda191614bf3",
        name="親子試乗体験会(有料)",
        description="親子で馬に乗る体験会です(競走馬ではりません)。",
        image_url="/images/event/9c1eac87-ce95-40ba-835f-913ef9f77eba.png",
        date="",
    ),
    EventSchema(
        category="horce-race",
        id="48a1da76-5910-4fb6-bd41-a53abb2c268c",
        name="第20番レース結果",
        description="1番は馬太郎。2番はホー助。3番は。。。",
        image_url="/images/event/9cbecd7e-4ed7-45b0-98a1-383869284ec1.png",
        date="",
    ),
    EventSchema(
        category="horce-race",
        id="98c25a03-18ee-43c1-a421-d547b04f4489",
        name="ジョッキーインタビュー",
        description="いちばん大切なのは馬と心を通わせることですね。",
        image_url="/images/event/33c07da0-3b7c-4873-bb80-c4b7e0fc2ff9.png",
        date="",
    ),
    EventSchema(
        category="bike-race",
        id="ae630e8d-fcdc-4493-8832-6288d1cd9f44",
        name="第30番レース結果",
        description="1番は田中。2番は山田",
        image_url="/images/event/54e5b9aa-4dae-4a50-b4e9-5f1f2bdaaaa0.png",
        date="",
    ),
    EventSchema(
        category="bike-race",
        id="8c1ce714-0c12-4660-861e-dc0dc14e60a7",
        name="選手インタビュー",
        description="毎日トレーニングに励んでいます。",
        image_url="/images/event/98f33add-da71-4917-9651-c5b351823935.png",
        date="",
    ),
    EventSchema(
        category="boat-race",
        id="5235716e-298a-4969-a09b-dcb79dcfed55",
        name="9月15日レース中止のお知らせ",
        description="台風のため中止します",
        image_url="/images/event/289ea0d4-d66f-4990-be01-e1ed01872157.png",
        date="",
    ),
    EventSchema(
        category="auto-race",
        id="68a08bfd-aa7c-42ab-82bc-f5fb492f9d6f",
        name="第5番レース結果",
        description="1番は田中。2番は山田",
        image_url="/images/event/4754e06d-f68a-4c64-9ba0-2c580d9787c5.png",
        date="",
    ),
    EventSchema(
        category="auto-race",
        id="30ed73da-c723-43bf-bcda-2bcc6734aa2c",
        name="選手インタビュー",
        description="プライベートではバイクに乗っていません。",
        image_url="/images/event/9405d9b6-cc25-42ff-b4b0-901aa32c6bc1.png",
        date="",
    ),
    EventSchema(
        category="horce-race",
        id="603094a7-2b99-4541-a5e0-c96a64c41f64",
        name="第8番レース結果",
        description="1番は田中。2番は山田",
        image_url="/images/event/b567ea66-be3a-41c0-a05d-3fa621d50382.png",
        date="",
    ),
]


class AbstractEventRepository(ABC):
    @abstractmethod
    def get_event_categories(self) -> list[str]:
        ...

    @abstractmethod
    def get_all_category_events(self) -> list[EventSchema]:
        ...

    @abstractmethod
    def get_category_events(self, category: str) -> list[EventSchema]:
        ...

    @abstractmethod
    def get_event(self, event_uuid: str) -> EventSchema:
        ...


class MockEventRepository(AbstractEventRepository):
    def __init__(self):
        self._events = pd.DataFrame([o.model_dump() for o in _EVENTS])

    def get_event_categories(self) -> list[str]:
        return _EVENT_CATEGORIES

    def get_all_category_events(self) -> list[EventSchema]:
        list_of_dicts = self._events.to_dict(orient="records")
        return [EventSchema.model_validate(d) for d in list_of_dicts]

    def get_category_events(self, category: str) -> list[EventSchema]:
        df = self._events[self._events["category"] == category]
        list_of_dicts = df.to_dict(orient="records")
        return [EventSchema.model_validate(d) for d in list_of_dicts]

    def get_event(self, event_uuid: str) -> EventSchema:
        result = self._events[self._events["id"] == event_uuid]
        if len(result) == 0:
            raise Exception("event not found")
        d = result.to_dict(orient="records")[0]
        return EventSchema.model_validate(d)


class AbstractImageRepository(ABC):
    @abstractmethod
    def get(self, file_name: str) -> io.BytesIO:
        ...


class LocalImageRepository(ABC):
    def __init__(self, root_path: str):
        self._root_path = root_path

    def get(self, file_name: str) -> io.BytesIO:
        file_path = os.path.join(self._root_path, file_name)
        if not os.path.isfile(file_path):
            raise ClientException("image not found")
        with open(file_path, "rb") as fin:
            data = fin.read()
        return io.BytesIO(data)
