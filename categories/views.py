from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import CategoryForm
from .models import Category
from .serializers import CategorySerializer


class CreateCategory(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return Response(template_name='categories/add_category.html', data={
            "form": CategoryForm,
        })

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class()
        data_from_request = request.data.copy()
        data_from_request["user"] = request.jwt_user
        validated_data = serializer_class.validate(data_from_request)
        try:
            serializer_class.create(validated_data)
        except Exception as e:
            messages.add_message(request, messages.INFO, "sdcsdc")

        return redirect("categories-list")


class CategoryList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        if request.jwt_user:

            return Response(template_name='categories/category_list.html', data={
                "categories": Category.objects.filter(user=request.jwt_user),
            })


class CategoryDetailView(APIView):
    headers = {'Content-Type': 'application/json'}
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'categories/category_detail.html'

    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        response = Response(data={
            'category': category,
        })
        return response


class CategoryDeleteView(APIView):
    model = Category
    success_url = '/'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        user = request.jwt_user
        category_to_delete = Category.objects.get(pk=pk)

        if user != category_to_delete.user:
            return 403

        response = Response(template_name='categories/category_confirm_delete.html', data={
            "category": category_to_delete
        })

        return response

    def post(self, request, pk, *args, **kwargs):

        user = request.jwt_user
        category_to_delete = Category.objects.get(pk=pk)

        if user != category_to_delete.user:
            return 403

        category_to_delete.delete()
        messages.add_message(request, messages.SUCCESS, f'Deleted {category_to_delete.name}')

        return redirect('categories-list')


class CategoryUpdateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = CategorySerializer

    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        form = CategoryForm(instance=category)
        response = Response(template_name='categories/add_category.html', data={
            "form": form
        })

        return response

    def post(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        form_data = CategoryForm(request.POST or None, instance=category)
        if form_data.is_valid():
            form_data.save()

            return redirect('categories-list')
