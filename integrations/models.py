from django.contrib.auth.models import User
from django.db import models


class Integration(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=400, null=True, blank=True)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    user_integration_info = models.JSONField("UserIntegrationInfo")

    def __str__(self):
        return f"Integration with {self.integration.type}, user - " \
               f"{self.user.username}"

    @property
    def type_of_integration(self):
        return self.integration.type
