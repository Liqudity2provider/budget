from rest_framework import serializers

from actions.models import Action
from budget_django.utils import get_keys
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer of Category model
    """

    # password = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        category = Category.objects.create(
            **validated_data
        )
        category.save()
        return category

    def validate(self, data):
        fields = self.Meta.model._meta.concrete_fields
        data = get_keys(fields, data)
        return data

    class Meta:
        model = Action

