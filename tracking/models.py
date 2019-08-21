from django.db import models


class TrackingInfo(models.Model):
    user_agent = models.CharField(max_length=512)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
