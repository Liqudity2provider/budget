from django.urls import path

from categories.views import CategoryList

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='categories_list'),

]
