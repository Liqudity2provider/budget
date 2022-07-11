from django.contrib import messages
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import ActionForm
from .models import Action
from .serializers import ActionSerializer


class ActionCreate(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ActionSerializer

    def get(self, request, *args, **kwargs):
        return Response(template_name='actions/action_post.html', data={
            "form": ActionForm,
        })

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class()
        validated_data = serializer_class.validate(request.data)
        try:
            serializer_class.create(validated_data)
        except Exception as e:
            messages.add_message(request, messages.INFO, "sdcsdc")

        return Response(template_name='budget_django/login.html', data={
            "form": ActionForm(),
            "messages": messages
        })


class ActionList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ActionSerializer

    def get(self, request, *args, **kwargs):
        if request.jwt_user:
            return Response(template_name='actions/action_list.html', data={
                "actions": Action.objects.filter(user=request.jwt_user),
            })

