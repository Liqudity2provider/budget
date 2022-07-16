from rest_framework import serializers

from actions.models import Action
from budget_django.utils import get_keys
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer of Category model
    """

    def create(self, validated_data):
        category = Category.objects.create(
            **validated_data
        )
        category.save()
        return category

    def validate(self, data):
        fields = [f.name for f in self.Meta.model._meta.get_fields()]
        data = get_keys(fields, data)
        return data

    class Meta:
        model = Action

