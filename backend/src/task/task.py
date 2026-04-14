import asyncio
from celery import Celery
from src.task import file_processing
from src.env import env

celery_app = Celery("file_tasks", broker=env.REDIS_URL, backend=env.REDIS_URL)

_worker_loop: asyncio.AbstractEventLoop | None = None

def run_in_worker_loop(coroutine):
    global _worker_loop
    if _worker_loop is None or _worker_loop.is_closed():
        _worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_worker_loop)
    return _worker_loop.run_until_complete(coroutine)


@celery_app.task
def process_file(file_id: str) -> None:
    run_in_worker_loop(file_processing.process_file(file_id))