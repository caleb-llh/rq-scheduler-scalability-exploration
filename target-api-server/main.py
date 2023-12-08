from datetime import datetime, timedelta
from time import sleep
import logging
import os

from fastapi import Depends, FastAPI, Request, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Scheduler API for ingestion pipeline",
    description="Scheduler for ingestion pipeline",
    ## set based on whatever is specified in nginx. Root path of static file server for swagger docs
    root_path="/",
)


logger = logging.getLogger(__name__)

@app.post(
    "/alarm"
    )
async def add_job(): 
    print(datetime.now())
    return JSONResponse(status_code=status.HTTP_201_CREATED,content=str(datetime.now()))
    



