from rest_framework import serializers
from .models import Moniurl, Log

class NewURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moniurl
        fields = '__all__'


class ListURLSerializer(serializers.ModelSerializer):

    class Meta:
        model = Moniurl
        fields = ['id', 'description', 'isAPI', 'httpMethod', 'url', 'entered_on']
