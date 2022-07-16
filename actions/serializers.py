from rest_framework import serializers

from actions.models import Action
from budget_django.utils import get_keys


class ActionSerializer(serializers.ModelSerializer):
    """
    Serializer of Action model
    """

    # password = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)

    def create(self, validated_data):
        action = Action.objects.create(
            **validated_data
        )
        action.save()
        return action

    def validate(self, data):
        fields = self.Meta.model._meta.concrete_fields
        data = get_keys(fields, data)
        return data

    class Meta:
        model = Action
        fields = ['__all__']
