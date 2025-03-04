"""
Serializers for famTree API's.
"""
from rest_framework import serializers

from core.models import Member
from famTree.models import Events, Location


class LocationSerializer(serializers.ModelSerializer):
    """ Serializer for location"""

    class Meta:
        model = Location
        fields = ["id", "name", "city", "street", "number",
                  "postal_code", "country", "lat", "long"]
        read_ony_fields = ["id"]

    def create(self, validated_data):
        """ Create a member."""
        events = validated_data.pop("event", [])
        auth_user = self.context["request"].user
        validated_data["editor"] = auth_user
        member = Member.objects.create(**validated_data)
        for event in events:
            Events.objects.get_or_create(
                editor=auth_user,
                **event,
            )
            # member.events.add(event_obj)

        return member


class EventSerializer(serializers.ModelSerializer):
    """ Serializer for event"""
    # location = LocationSerializer(required=False)

    class Meta:
        model = Events
        fields = ["id", "member", "event_type", "date", "source"]
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

    def _get_or_create_events(self, events, member, auth_user):

        for event in events:
            event_obj = Events.objects.get_or_create(
                editor=auth_user,
                **event,
            )
            member.events.add(event_obj)

    def create(self, validated_data):
        """ Create a member."""
        events = validated_data.pop("events", [])
        auth_user = self.context["request"].user
        validated_data["editor"] = auth_user
        member = Member.objects.create(**validated_data)
        self._get_or_create_events(events, member, auth_user)

        return member

    def update(self, instance, validated_data):
        """ Update existing member by ID."""
        events = validated_data.pop("events", None)
        auth_user = self.context["request"].user
        validated_data["editor"] = auth_user

        if events is not None:
            instance.events.clear()
            self._get_or_create_events(events, instance, auth_user)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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
