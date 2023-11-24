from fastapi import FastAPI
import uvicorn
from eventapp.controller import Router
from eventapp.di import DiContainer


def main(app: FastAPI):
    dic = DiContainer()
    event_service, image_service = dic.get_services()
    router = Router(event_service, image_service)
    app.include_router(router)


app = FastAPI()
main(app)

if __name__ == "__main__":
    uvicorn.run(app)
