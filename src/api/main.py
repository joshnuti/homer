from fastapi import FastAPI, Security
from .helpers.logging import logger
from .helpers.security import authorize
from .helpers.file import verify_config_exists, copy_defaults, read_config
from .helpers.ids import assign_missing_ids
from .models.config import Config
from .routers import config, links, replace, services

app = FastAPI(
    title="Homer API",
    version="Dev",
    description="Icon prefix: 'fas fa-'",
)

app.include_router(config.router, dependencies=[Security(authorize)])
app.include_router(replace.router, dependencies=[Security(authorize)])
app.include_router(links.router, dependencies=[Security(authorize)])
app.include_router(services.router, dependencies=[Security(authorize)])


@app.on_event("startup")
def startup_event():
    logger.info("==== Starting API ===========")

    if not verify_config_exists():
        logger.info("config.yml file not find. Copying defaults.yml")

        try:
            copy_defaults()
        except FileNotFoundError:
            logger.error(
                'Unable to copy defaults.yml to config.yml. Please use /config/replace to upload a config file')
        except:
            logger.error(
                'Error trying to copy defaults.yml to config.yml. Please use /config/replace to upload a config file')
            
    config = Config(**read_config())
    assign_missing_ids(config.links)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("==== Closing API  ===========")


@app.get("/", include_in_schema=False)
async def ping():
    return {"message": "Hello World"}
