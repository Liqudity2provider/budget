from django.urls import path

from categories.views import CategoryList, CreateCategory, CategoryDetailView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='categories-list'),
    path('category_create/', CreateCategory.as_view(), name='create-category'),
    path('category/<pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('category/<pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),

]
