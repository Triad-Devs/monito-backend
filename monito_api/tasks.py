from celery import shared_task
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from .models import Log, Moniurl
from .utils import Util

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


    url = Moniurl.objects.get(pk=url_id) 

    if r.status_code >= 400 and r.status_code <=599:
        url.failedCount +=1
        url.save()
        if url.failedCount >= url.alertThreshold:
            email_body = 'Hi '+ url.user.first_name +',\n\nWe have noticed some irregularities in your URL.\nBelow are the details:\nURL: '+url.url+'\nMethod: '+url.httpMethod+'\nAlert Threshold: '+str(url.alertThreshold)+'\n\nRegards Monito,\nBy Team Triad'
            to_email = url.user.email
            data = {'email_body': email_body, 'to_email': to_email,
                'email_subject': r'Monito Alert! {}'.format(url.url)}
            Util.send_email(data)
            url.failedCount = 0
            url.save()
    else:
        url.failedCount = 0
        url.save()



    log = Log(
        url = url,
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