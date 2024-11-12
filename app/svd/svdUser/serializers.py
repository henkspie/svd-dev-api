"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class SvdUserSerializer(serializers.ModelSerializer):
    """ Serializer for the svdUser object."""
    name = serializers.ReadOnlyField()
    birthday = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ['birthday', 'name', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """ Create and return a svdUser with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
