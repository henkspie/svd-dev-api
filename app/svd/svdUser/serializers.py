"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class SvdUserSerializer(serializers.ModelSerializer):
    """ Serializer for the svdUser object."""

    class Meta:
        model = get_user_model()
        fields = ['svdUser', 'name', 'birthday', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ['svdUser']

    def create(self, validated_data):
        """ Create and return a svdUser with encrypted password."""
        # print(validated_data)
        name = validated_data['name']
        birthday = validated_data['birthday']
        email = validated_data['email']
        password = validated_data['password']

        del validated_data['name']
        del validated_data['birthday']
        del validated_data['email']
        del validated_data['password']
        # print(validated_data)
        return get_user_model().objects.create_user(name, birthday,
                                                    password, email,
                                                    **validated_data)
