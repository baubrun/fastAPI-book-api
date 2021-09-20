from fastapi import FastAPI
from .containers import Container
from . import routes


def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[routes])

    db = container.db()
    db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(routes.router)
    return app


app = create_app()

