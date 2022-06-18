from celery import shared_task
import requests
from datetime import datetime


@shared_task(bind=True)
def send_request_func(self, api):
    response = requests.get(api)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(api, response)