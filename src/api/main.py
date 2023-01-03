from fastapi import FastAPI, Security
from .helpers.logging import logger
from .helpers.security import authorize
from .helpers.file import verify_config_path, copy_defaults, write_config, read_config
from .routers import config, file, links, services
from .helpers.exceptions import EmptyFileError

app = FastAPI(
    title="Homer API",
    version="Dev",
    description="Icon prefix: 'fas fa-'",
)

app.include_router(config.router, dependencies=[Security(authorize)])
app.include_router(file.router, dependencies=[Security(authorize)])
app.include_router(links.router, dependencies=[Security(authorize)])
app.include_router(services.router, dependencies=[Security(authorize)])


@app.on_event("startup")
def startup_event():
    logger.info("==== Starting API ===========")

    try:
        write_config(None, read_config(None))
    except FileNotFoundError:
        logger.info('No file found. Writing defaults')
        copy_defaults(None)
    except EmptyFileError:
        logger.info('Empty file found. Writing defaults')
        copy_defaults(None)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("==== Closing API  ===========")


@app.get("/", include_in_schema=False)
async def ping():
    return {"message": "Hello World"}
