from celery import shared_task
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from .models import Log, Moniurl


@shared_task(bind=True)
def send_request_func(self, url_id, url, httpMethod, JSONbody, bearer):


    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + bearer


    # print(type(headers))
    # print(headers)
    # print(type(JSONbody))
    # print(JSONbody)

    if httpMethod == 'GET':
        r = requests.get(url, headers=headers)

    if httpMethod == 'POST':
        r = requests.post(url, headers=headers, data=JSONbody)

    if httpMethod == 'PUT':
        r = requests.put(url, headers=headers, data=JSONbody)

    if httpMethod == 'PATCH':
        r = requests.patch(url, headers=headers, data=JSONbody)


    if httpMethod == 'DELETE':
        r = requests.delete(url, headers=headers)



    log = Log(
        url = Moniurl.objects.get(pk=url_id),
        req_url = r.url,
        status_code = r.status_code,
        content_length = len(r.content),
        time_taken = r.elapsed.total_seconds(),
        content_type = r.headers['Content-Type'])
    log.save()



    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time: " + current_time + "  " + str(url_id) + "  " + str(r.url) + "  " + str(r.status_code))
    print("==========================")