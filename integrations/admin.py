from django.contrib import admin

# Register your models here.
from integrations.models import UserIntegration, Integration

admin.site.register(UserIntegration)
admin.site.register(Integration)
