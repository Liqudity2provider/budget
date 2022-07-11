from django import forms

from actions.models import Action
from categories.models import Category


class ActionForm(forms.ModelForm):
    """
    Form for creating Action model
    """

    name = forms.CharField()
    description = forms.CharField(required=False, widget=forms.Textarea)
    amount = forms.IntegerField(required=False)
    # category = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(user=self.user))
    income = forms.BooleanField()
    date = forms.DateTimeField(required=False)
    details = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, user=None, *args, **kwargs):
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

        super(ActionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Action
        fields = "__all__"
        exclude = ('user',)

