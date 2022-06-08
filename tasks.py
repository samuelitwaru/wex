from wex.celery import app


@app.task
def debug_task(self):
    import time
    time.sleep(5)
    print(f'Request: {self.request!r}')