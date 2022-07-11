from django.urls import path

from actions.views import ActionList, ActionCreate

urlpatterns = [
    path('actions/', ActionList.as_view(), name='actions_list'),
    path('action_create/', ActionCreate.as_view(), name='create_action'),
    path('action/<pk>', ActionList.as_view(), name='action-detail'),
]
