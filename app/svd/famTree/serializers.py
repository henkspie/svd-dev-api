"""
Serializers for famTree API's.
"""
from rest_framework import serializers

from core.models import Member


class MemberSerializer(serializers.ModelSerializer):
    """ Serializer for member."""

    class Meta:
        model=Member
        fields = [
            "id",
            "lastname",
            "firstname",
            "call_name",
            "sex",
            "birthday",
            "birthday_txt",
            "father",
            "mother",
            "editor",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """ Create a member."""
        return Member.objects.create(**validated_data)

