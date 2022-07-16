import datetime

from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ActionForm
from .models import Action
from .serializers import ActionSerializer


class ActionCreate(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ActionSerializer

    def get(self, request, *args, **kwargs):
        form = ActionForm(request.GET, user=request.jwt_user)
        return Response(template_name='actions/action_post.html', data={
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        serializer_class = self.serializer_class()
        form_data = ActionForm(request.POST, user=request.jwt_user)
        if form_data.is_valid():
            clean = form_data.cleaned_data.copy()
            clean["user"] = request.jwt_user
            validated_data = serializer_class.validate(clean)
            try:
                serializer_class.create(validated_data)
            except Exception as e:
                messages.add_message(request, messages.SUCCESS, f'Error {e.args[0]}')

            return redirect('actions_list')


class ActionList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ActionSerializer

    def get(self, request, *args, **kwargs):
        if request.jwt_user:
            return Response(template_name='actions/action_list.html', data={
                "actions": Action.objects.filter(user=request.jwt_user).order_by("-date"),
            })


class ActionDetailView(APIView):
    headers = {'Content-Type': 'application/json'}
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'actions/action_detail.html'

    def get(self, request, pk):
        action = Action.objects.get(pk=pk)
        response = Response(data={
            'action': action,
        })
        return response


class ActionDeleteView(APIView):
    model = Action
    success_url = '/'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk, *args, **kwargs):
        user = request.jwt_user
        action_to_delete = Action.objects.get(pk=pk)

        if user != action_to_delete.user:
            return 403

        response = Response(template_name='actions/action_confirm_delete.html', data={
            "action": action_to_delete
        })

        return response

    def post(self, request, pk, *args, **kwargs):

        user = request.jwt_user
        action_to_delete = Action.objects.get(pk=pk)

        if user != action_to_delete.user:
            return 403

        action_to_delete.delete()

        return redirect('actions_list')


class ActionUpdateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ActionSerializer

    def get(self, request, pk, *args, **kwargs):
        user = request.jwt_user
        action = Action.objects.get(pk=pk)
        form = ActionForm(instance=action, user=user)
        response = Response(template_name='actions/action_post.html', data={
            "form": form
        })

        return response

    def post(self, request, pk, *args, **kwargs):
        action = Action.objects.get(pk=pk)
        form_data = ActionForm(request.POST or None, user=request.jwt_user, instance=action)
        if form_data.is_valid():
            form_data.save()
            return redirect('actions_list')

