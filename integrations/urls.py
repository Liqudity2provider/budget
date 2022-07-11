from django.urls import path

from integrations.views import MonoIntegration, AllIntegrations, \
    UploadStatisticFromBank

urlpatterns = [
    path('mono/', MonoIntegration.as_view(), name="mono-integration"),
    path('manage_bank_account/', AllIntegrations.as_view(),
         name="manage_bank_account"),
    path('upload_statistic_from_bank/<pk>', UploadStatisticFromBank.as_view(),
         name="upload_statistic_from_bank"),

]
