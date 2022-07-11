from django.contrib import messages
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import CategoryForm
from .models import Category
from .serializers import CategorySerializer


class CreateCategory(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return Response(template_name='budget_django/register.html', data={
            "form": CategoryForm,
        })

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class()
        validated_data = serializer_class.validate(request.data)
        try:
            serializer_class.create(validated_data)
        except Exception as e:
            messages.add_message(request, messages.INFO, "sdcsdc")

        return Response(template_name='budget_django/login.html', data={
            "form": CategoryForm(),
            "messages": messages
        })


class CategoryList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if request.jwt_user:
            return Response(template_name='categories/category_list.html', data={
                "categories": Category.objects.filter(user=request.jwt_user),
            })
