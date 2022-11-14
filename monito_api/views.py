import multiprocessing as mp

import django
django.setup()

from time import time
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

from django.db.models.functions import TruncDay
from django.db.models import Count, Avg, Sum


from statistics import mean

from django. conf import settings
import os




def traffic_graph(data, user_dir_path, logs, daily_logs_list):
    print(data)
    import matplotlib.pyplot as plt

    #Traffic Graph
    traffic_graph_path = os.path.join(user_dir_path, "traffic_graph.png")
    if os.path.exists(traffic_graph_path):
        os.remove(traffic_graph_path)
        print("Removed")

    print("traffic_graph_path", traffic_graph_path)

    date_list = []
    date_list = [logs[p]['day'].strftime("%m/%d/%y") for p in range(len(logs))]
    
    plot1=plt.figure(1)
    plt.bar(date_list, daily_logs_list)
    
    plt.xlabel('Date')
    plt.ylabel('Total Bytes Transferred')
    
    plt.title('Traffic Graph')
    plt.savefig(traffic_graph_path, dpi=300)

    plt.close()
    plt.figure().clear()



def response_time_graph(data, user_dir_path, no_of_requests, req):
    print(data)
    import matplotlib.pyplot as plt

    #Response time graph
    response_time_graph_path = os.path.join(user_dir_path, "response_time_graph.png")
    if os.path.exists(response_time_graph_path):
        os.remove(response_time_graph_path)
        print("Removed")

    print("response_time_graph_path", response_time_graph_path)

    response_time_list = []
    response_time_list = [x.time_taken for x in req]

    requests_number_list = []
    requests_number_list = [s for s in range(1, no_of_requests+1)]

    plot2 = plt.figure(2)
    plt.plot(requests_number_list, response_time_list, marker = 'x')

    plt.xlabel('Requests Number')
    plt.ylabel('Response Time(s)')
    
    plt.title('Response Time Graph')
    plt.savefig(response_time_graph_path, dpi=300)

    plt.close()
    plt.figure().clear()





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




class CurrentURLView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, url_id):

        try:
            url_data = Moniurl.objects.get(pk=url_id, user=request.user)
        except ObjectDoesNotExist:
            return Response({'response':'Invalid URL ID'})

        url = url_data.url
        httpMethod = url_data.httpMethod
        JSONbody = url_data.JSONbody
        bearer = url_data.bearer
        isAPI = url_data.isAPI

        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer " + bearer


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

        status_code = r.status_code
        status_text = r.reason
        content_length = len(r.content)
        time_taken = r.elapsed.total_seconds()
        content_type = r.headers['Content-Type']

        if(isAPI):
            jsonBody = r.json()
        else:
            jsonBody = None

        return Response({
            "isAPI": isAPI,
            "httpMethod": httpMethod,
            "status_code": status_code,
            "status_text": status_text,
            "content_length": content_length,
            "time_taken": time_taken,
            "content_type": content_type,
            "jsonBody": jsonBody,
        }, status=status.HTTP_200_OK)




class StatisticsView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, url_id):

        # DON'T DELETE THE COMMENTS

        # The monitoring statistics endpoint response must contain the following:
        #    - Total requests
        #    - Number of successful requests (200, 201, etc)
        #    - Number of failed requests (detect using status codes like 500, 404, etc)
        #    - Error rate % (failed requests / total requests * 100)
        #    - Success rate % (100 - Error rate)
        #    - Average response time
        #    - Response time Vs Time Graph
        #    - Total bytes transferred
        #    - Bytes transferred PER REQUESTS PER DAY 
        #    - Average bytes transferred PER DAY
        #    - Peak Traffic date (max of daily bytes transferred)
        #    - Bytes transferred daily Vs Time Graph = Traffic Graph

        requests = Log.objects.filter(url = url_id)
        no_of_requests = len(requests)
        success_requests = 0
        failed_requests = 0
        total_response_time = 0
        total_bytes = 0
        for i in requests:
            if i.status_code >= 200 and i.status_code <=299:
                success_requests+=1
            if i.status_code >= 400 and i.status_code <=599:
                failed_requests+=1
            total_response_time+=i.time_taken
            total_bytes+=i.content_length

        error_rate = failed_requests/no_of_requests*100

        success_rate = 100-error_rate

        avg_response_time = total_response_time/no_of_requests

        logs = Log.objects.annotate(day=TruncDay('entered_on')).values('day').annotate(count=Count('url'), avg_bytes_transferred=Avg('content_length'), total_bytes_transferred=Sum('content_length')).values('day', 'count', 'url', 'avg_bytes_transferred', 'total_bytes_transferred').filter(url=url_id)
        daily_logs_list = [logs[p]['total_bytes_transferred'] for p in range(len(logs))]
        avg_bytes_transferred = mean(daily_logs_list)
        max_of_daily_bytes_transferred = max(daily_logs_list)

        #graphs
        user_dir_path = os.path.join(settings.MEDIA_ROOT, r"{}{}".format(request.user.id, url_id))
        if not os.path.exists(user_dir_path):
            os.mkdir(user_dir_path)
            print(user_dir_path)


        p1 = mp.Process(target=traffic_graph, args=("works", user_dir_path, logs, daily_logs_list))
        p2 = mp.Process(target=response_time_graph, args=("works", user_dir_path, no_of_requests, requests))
        p1.start()
        p2.start()
        p1.join()
        p2.join()


        return Response({
            "url_id": url_id,
            "total_requests" : no_of_requests,
            "success_requests": success_requests,
            "failed_requests": failed_requests,
            "error_rate(%)": error_rate,
            "success_rate(%)": success_rate,
            "avg_response_time(s)": avg_response_time,
            "total_bytes_transferred": total_bytes,
            "per_day_stats": logs,
            "avg_bytes_transferred_per_day": avg_bytes_transferred,
            "max_of_daily_bytes_transferred": max_of_daily_bytes_transferred,
            "traffic_graph_url": r"https://monito-backend-production.up.railway.app/media/{}{}/traffic_graph.png".format(request.user.id, url_id),
            "response_time_graph_url": r"https://monito-backend-production.up.railway.app/media/{}{}/response_time_graph.png".format(request.user.id, url_id),
            }, status=status.HTTP_200_OK)