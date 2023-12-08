from datetime import datetime, timedelta
from time import sleep
import logging
import os
import requests

from fastapi import Depends, FastAPI, Request, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

app = FastAPI(
    title="Scheduler API for ingestion pipeline",
    description="Scheduler for ingestion pipeline",
    ## set based on whatever is specified in nginx. Root path of static file server for swagger docs
    root_path="/",
)


logger = logging.getLogger(__name__)
jobstores = {
    'default': RedisJobStore(host='redis', port=6379)
}
scheduler = BackgroundScheduler(
    jobstores=jobstores, 
    daemon=True,
    logger=logger
    )
scheduler.start()

INITIAL_SLEEP_SECONDS = int(os.getenv('INITIAL_SLEEP_SECONDS'))
TIMER_SECONDS = int(os.getenv('TIMER_SECONDS'))

def alarm():
    url = 'http://{ip}:{port}/alarm'.format(
        ip='api-server',
        port='15565',
    )
    result = requests.post(url)
    logger.info(f"result: {result}")
    return result



@app.post(
    "/add"
    )
async def post_add_job(): 
    JOB_ID = 'test_job_id'
    print(f"sleeping for {INITIAL_SLEEP_SECONDS} seconds")
    sleep(INITIAL_SLEEP_SECONDS)
    print(f"finished sleeping, adding job")
    print(datetime.now())

    scheduler.add_job(
        alarm, 
        id=JOB_ID,
        trigger='interval', 
        seconds=TIMER_SECONDS,
        replace_existing=True,
        # ensure job runs only once instead of every TIMER_SECONDS
        start_date=str(datetime.now()),
        end_date=str(datetime.now() + timedelta(seconds=TIMER_SECONDS*1.5))
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED,content=str(datetime.now()))
    



