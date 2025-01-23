"""Main init file for FastAPI project datacite-to-opendataswiss."""

import logging
import sys
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

# from fastapi.middleware.cors import CORSMiddleware
# from app.config import config_app, log_level
from app.routers import converters


# TODO finish WIP
# TODO create Settings
# TODO remove unused code

# TODO review logging configuration
# Setup logging
logging.basicConfig(
    level="WARNING",
    format=(
        "%(asctime)s.%(msecs)03d [%(levelname)s] "
        "%(name)s | %(funcName)s:%(lineno)d | %(message)s"
    ),
    datefmt="%y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)


# TODO read values from pyproject.toml
def get_application() -> FastAPI:
    """Create app instance using config_app."""
    _app = FastAPI(
        title="datacite-to-opendataswiss",
        description="API that converts metadata in DataCite XML format to "
        "opendata.swiss XML format.",
        version="0.1.0",
        license_info={
            "name": "MIT",
            "url": "https://github.com/eawag-rdm/datacite-to-opendataswiss/blob/main/LICENSE",
        },
        debug=False,
        root_path="",
    )

    # _app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=[str(config_app.CORS_ORIGIN)],
    #     allow_headers=["*"],
    # )

    return _app


# Create app instance
app = get_application()

# Add routers
app.include_router(converters.router)

# TODO create error_router
# app_router.include_router(error_router)


# Redirect home path to documentation
@app.get("/", include_in_schema=False)
async def home():
    """Redirect home to docs."""
    return RedirectResponse(f"/docs")
