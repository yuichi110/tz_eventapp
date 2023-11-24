from pydantic import BaseModel


class EventSchema(BaseModel):
    id: str
    name: str
    category: str
    description: str
    image_url: str
    date: str
