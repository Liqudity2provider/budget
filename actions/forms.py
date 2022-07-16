from django import forms

from actions.models import Action
from categories.models import Category


class ActionForm(forms.ModelForm):
    """
    Form for creating Action model
    """
    category = forms.ModelMultipleChoiceField(required=False, queryset=Action.objects.none(),
                                              widget=forms.CheckboxSelectMultiple())
    date = forms.DateTimeField(required=True, widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        if "user" not in kwargs:
            raise KeyError("There is no user defined for ActionForm")
        self.base_fields["category"].queryset = Category.objects.filter(user=kwargs.pop("user"))
        super(ActionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Action
        fields = "__all__"
        exclude = ('user',)
