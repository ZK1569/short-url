import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import APIRouter, FastAPI

from src.controllers.admin import router as admin_router
from src.controllers.health import router as health_router
from src.controllers.url import router as url_router
from src.utils.database.postgres import postgresql_database


def main():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        try:
            postgresql_database.setup_database()
        except Exception as e:
            sys.exit(f"❌ Error: {e}")
        yield

    app = FastAPI(lifespan=lifespan)

    api = APIRouter(prefix="/v1")

    api.include_router(health_router)
    api.include_router(url_router)
    api.include_router(admin_router)

    app.include_router(api)

    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
