from django import forms

from categories.models import Category


class CategoryForm(forms.ModelForm):
    """
    Form for creating Category model
    """

    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('user',)
