"""
Serializers for famTree API's.
"""
from rest_framework import serializers

from core.models import Member
from famTree.models import Event


class EventSerializer(serializers.ModelSerializer):
    """ Serializer for event"""

    class Meta:
        model = Event
        fields = ["id", "member", "event_type", "date", "place", "source"]
        read_ony_fields = ["id"]


class MemberSerializer(serializers.ModelSerializer):
    """ Serializer for member."""
    events = EventSerializer(many=True, required=False)

    class Meta:
        model = Member
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
            "events",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """ Create a member."""
        events = validated_data.pop("event", [])
        auth_user = self.context["request"].user
        validated_data["editor"] = auth_user
        member = Member.objects.create(**validated_data)
        for event in events:
            Event.objects.get_or_create(
                editor=auth_user,
                **event,
            )
            # member.events.add(event_obj)

        return member

    # def update(self, instance, validated_data):
    #     """ Update existing member by ID."""

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance


class MemberDetailSerializer(MemberSerializer):
    """ Serializer for member detail view."""

    class Meta(MemberSerializer.Meta):
        fields = MemberSerializer.Meta.fields + ['note', 'editor']


class MemberImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to member."""

    class Meta:
        model = Member
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
