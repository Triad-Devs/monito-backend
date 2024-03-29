from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Moniurl(models.Model):
    
    def JSON_default():
        return {}

        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    description = models.CharField(max_length=100, blank=True)
    isAPI = models.BooleanField()
    repeatAfter = models.IntegerField()
    httpMethod = models.CharField(max_length=10)
    url = models.CharField(max_length=100)
    JSONbody = models.JSONField(default=JSON_default)
    authReq = models.BooleanField()
    bearer = models.CharField(max_length=100, blank=True)
    entered_on = models.DateTimeField(auto_now_add=True)
    failedCount = models.IntegerField(default=0)
    alertThreshold = models.IntegerField()


    def __str__(self):
        return f"{self.user}__{self.httpMethod}__{self.url}"


class Log(models.Model):
    url = models.ForeignKey(Moniurl, on_delete=models.CASCADE, related_name='moni_url')
    req_url = models.CharField(max_length=100)
    status_code = models.IntegerField()
    content_length = models.IntegerField()
    time_taken = models.DecimalField(max_digits=19, decimal_places=7)
    content_type = models.CharField(max_length=30)
    entered_on = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.url}__{self.status_code}"