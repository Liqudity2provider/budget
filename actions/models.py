from django.contrib.auth.models import User
from django.db import models
from categories.models import Category


class Action(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=400, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    category = models.ManyToManyField(Category, null=True, blank=True)
    income = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateTimeField()
    details = models.TextField(max_length=400, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
