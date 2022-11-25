from fastapi import FastAPI
from .helpers.logging import logger
from .routers import defaults, links, services, config

logger.info("==== Starting API ===========")

app = FastAPI(title="Homer API", version="Dev")

app.include_router(links.router)
app.include_router(services.router)
app.include_router(defaults.router)
app.include_router(config.router)


@app.on_event("shutdown")
def shutdown_event():
    logger.info("==== Closing API  ===========")


@app.get("/")
async def ping():
    return {"message": "Hello World"}
