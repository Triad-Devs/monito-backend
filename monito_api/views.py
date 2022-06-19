from django.shortcuts import render

from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

import json
import random
from datetime import datetime

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import (
    NewURLSerializer
)

from django.core.exceptions import ObjectDoesNotExist



# Create your views here.

class TestView(generics.GenericAPIView):

    def get(self, request):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=3,
            period=IntervalSchedule.MINUTES,
        )
        task = PeriodicTask.objects.create(interval=schedule, name="send_request_task_"+str(random.randint(3,100)), task='monito_api.tasks.send_request_func', args=json.dumps([1, 'https://jsonplaceholder.typicode.com/todos/1', 'GET', {}, ""]))
        return Response({'resp': "It's Working"}, status=status.HTTP_200_OK)



