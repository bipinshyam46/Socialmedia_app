from rest_framework import serializers
from .models import *

class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    