from django import forms

from integrations.models import UserIntegration


class UserIntegrationForm(forms.ModelForm):
    """
    Form for creating UserINTEGRATION model
    """

    class Meta:
        model = UserIntegration
        fields = "__all__"
        exclude = ('user',)
