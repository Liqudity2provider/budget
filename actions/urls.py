from django.urls import path

from actions.views import ActionList, ActionCreate, ActionDetailView, ActionDeleteView, ActionUpdateView

urlpatterns = [
    path('actions/', ActionList.as_view(), name='actions_list'),
    path('action_create/', ActionCreate.as_view(), name='create_action'),
    path('action/<pk>', ActionDetailView.as_view(), name='action-detail'),
    path('action/<pk>/update', ActionUpdateView.as_view(), name='action-update'),
    path('action/<pk>/delete', ActionDeleteView.as_view(), name='action-delete'),
]
