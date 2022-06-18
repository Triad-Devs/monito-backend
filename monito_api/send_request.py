from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
import json
import random


def run():
    requests = [{'api':'https://catfact.ninja/fact', 'time': 1}, {'api':'https://dog.ceo/api/breeds/image/random', 'time': 2}, {'api':'https://randomuser.me/api/', 'time':4}]
    for i in requests:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=i['time'],
            period=IntervalSchedule.MINUTES,
        )
        task = PeriodicTask.objects.create(interval=schedule, name="send_request_task_"+str(random.randint(3,100)), task='monito_api.tasks.send_request_func', args=json.dumps([i['api']]))
    print('Done')
