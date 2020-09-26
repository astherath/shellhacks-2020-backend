from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from starlette.middleware.cors import CORSMiddleware

from config.main import (
    ALLOWED_ORIGINS,
    ALLOWED_HOSTS,
    ALLOWED_HEADERS,
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
)

from routes.users import router as users_router

app = FastAPI()


@app.get("/", status_code=200)
async def index():
    return {"ok": True}


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=ALLOWED_HEADERS,
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=ALLOWED_HOSTS,
)


# define a custom OpenAPI schem
def custom_schema():
    # chache the docs if they're already loaded
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# add routers
app.include_router(users_router)

# add schema for docs
app.openapi = custom_schema
