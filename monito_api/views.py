from django.shortcuts import render

from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

import json
import random
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime

from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import (
    NewURLSerializer,
    ListURLSerializer
)

from .models import Moniurl, Log

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



class NewURLView(generics.GenericAPIView):

    serializer_class = NewURLSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        # print(type(request.user))
        request.data['user']=request.user.pk
        # print(request.data)

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()


        url_data = serializer.data

        # print(url_data)

        url_id = url_data['id']
        url = request.data.get('url')
        httpMethod = request.data.get('httpMethod')
        repeatAfter = request.data.get('repeatAfter')
        JSONbody = request.data.get('JSONbody')
        bearer = request.data.get('bearer')


        schedule, created = IntervalSchedule.objects.get_or_create(
            every=repeatAfter,
            period=IntervalSchedule.MINUTES,
        )
        task = PeriodicTask.objects.create(interval=schedule, name="task_"+str(request.user.pk)+'_'+str(datetime.now().timestamp()), task='monito_api.tasks.send_request_func', args=json.dumps([url_id, url, httpMethod, JSONbody, bearer]))

        return Response(url_data, status=status.HTTP_201_CREATED)




class ListURLView(generics.GenericAPIView):

    serializer_class = ListURLSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        urls = Moniurl.objects.filter(user = request.user).order_by('entered_on')
        serializer = ListURLSerializer(instance=urls, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class GetURLDetailsView(generics.GenericAPIView):

    serializer_class = NewURLSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, url_id):

        try:
            url_data = Moniurl.objects.get(pk=url_id, user=request.user)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid URL ID'})
            
        serializer = NewURLSerializer(instance=url_data)

        return Response(serializer.data, status=status.HTTP_200_OK)