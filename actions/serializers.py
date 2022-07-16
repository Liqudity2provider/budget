from rest_framework import serializers

from actions.models import Action
from budget_django.utils import get_keys


class ActionSerializer(serializers.ModelSerializer):
    """
    Serializer of Action model
    """

    def create(self, validated_data):
        categories = validated_data.pop("category", [])
        action = Action.objects.create(
            **validated_data,
        )
        action.category.add(*categories)
        action.save()
        return action

    def validate(self, data):
        fields = [f.name for f in self.Meta.model._meta.get_fields()]
        data["income"] = True if data["income"] else False
        data = get_keys(fields, data)
        return data

    class Meta:
        model = Action
        fields = ['__all__']
