from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from integrations.forms import UserIntegrationForm
from integrations.integrations_manager import IntegrationManager
from integrations.models import UserIntegration, Integration


class MonoIntegration(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        mono_url = "https://api.monobank.ua/"
        return render(request, 'integrations/mono.html',
                      {
                          # 'image_path': image_path,
                          "mono_url": mono_url
                      })

    def post(self, request, *args, **kwargs):
        integration_class = Integration.objects.filter(name="monobank").first()
        if not integration_class:
            integration_class = Integration.objects.create(name="monobank", type="monobank")

        token = request.POST.get("token")
        # add validation for token
        user = request.jwt_user

        if not user:
            return 403

        integration = UserIntegration.objects.create(
            user=user,
            integration=integration_class,
            user_integration_info={"token": token}
        )

        messages.add_message(request, messages.SUCCESS, f'Added {integration.type_of_integration}')

        return render(request, 'integrations/mono_save_token.html',
                      {})


class AllIntegrations(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        if request.jwt_user:
            return Response(template_name='integrations/allintegrations_list'
                                          '.html',
                            data={
                                "user_integrations":
                                    UserIntegration.objects.filter(
                                        user=request.jwt_user),
                            })


class UploadStatisticFromBank(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    integration_manager = IntegrationManager

    def post(self, request, *args, **kwargs):
        if request.jwt_user:
            integration_manager_entity = self.integration_manager(user=request.jwt_user)
            try:
                integration_manager_entity.process_integrations()
            except Exception as e:
                messages.add_message(request, messages.INFO, f'Error: {e.args[0]}')

        return redirect(to="actions_list")


class UserIntegrationCreate(generics.CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        form = UserIntegrationForm(request.GET, user=request.jwt_user)
        return Response(template_name='integrations/userintegration_post.html', data={
            "form": form,
        })
