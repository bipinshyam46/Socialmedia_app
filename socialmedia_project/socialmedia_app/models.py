
from turtle import title
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime


# Create your models here.
class Users(AbstractUser):
    mobile=models.TextField(default='none',max_length=20)
    name=models.TextField(default='none')
    class Meta:
        db_table='Usertable'

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.CharField(max_length=100)
    title=models.TextField()
    description=models.TextField()
    tags=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)
    published_status=models.BooleanField(default=False)

    def __str__(self):
        return self.user

class Likepost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username