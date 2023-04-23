from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


class Quote(models.Model):
    quote = models.CharField()
    author = models.CharField()
    tags = ArrayField(models.CharField())
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
