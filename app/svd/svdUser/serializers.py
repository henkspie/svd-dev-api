"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext_lazy as _

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
        user = get_user_model().objects.create_user(name, birthday,
                                                    password, email,
                                                    **validated_data)
        # print(f"create: {user}")
        return user

    def update(self, instance, validated_data):
        """ Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """ Serializer for the user auth token."""
    svdUser = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """ Validate and authenticate the svdUser."""
        # print(f"attrs {attrs}")
        svdUser = attrs.get('svdUser')
        password = attrs.get('password')
        # print(f"in validate: {svdUser} {password}")
        user = authenticate(
            request=self.context.get('request'),
            username=svdUser,
            password=password,
        )
        # print(f"returned user: {user}")
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
