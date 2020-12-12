from rest_framework import serializers
from .models import *

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

class infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = info
        fields = '__all__'