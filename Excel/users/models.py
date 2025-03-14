from django.db import models
from django.contrib.auth.models import User
from utils.manager import ActiveManager

class UserProfile(models.Model):
    user_id = models.IntegerField()
    age = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    objects = ActiveManager()
