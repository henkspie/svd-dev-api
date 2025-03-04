"""
Views for the member APIs.
"""

from drf_spectacular.utils import (     # noqa: F401
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiTypes,
)
from rest_framework import viewsets, mixins, status     # noqa: F401
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Member
from famTree.models import Events, Location
from famTree import serializers

def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]


class MemberViewSet(viewsets.ModelViewSet):
    """ View for manage member API's."""

    serializer_class = serializers.MemberDetailSerializer
    queryset = Member.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Create a new member""" # @property
        serializer.save(editor=self.request.user)

    def perform_destroy(self, instance):
        if instance.editor == self.request.user:
            # print("Delete")
            instance.delete()
        # print("Not delete")
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        """ Retrieve all members and events."""
        events = self.request.query_params.get("Events")
        queryset = self.queryset
        if events:
            event_ids = self._params_to_ints(events)
            queryset = queryset.filter(event__id__in=event_ids)

        return queryset.order_by('birthday')

    def get_serializer_class(self):
        """ Return the serializer class for request"""
        if self.action == 'list':
            return serializers.MemberSerializer
        elif self.action == 'upload_image':
            return serializers.MemberImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to member."""
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventViewSet(viewsets.ModelViewSet):
    """ Manage events in the database """
    serializer_class = serializers.EventSerializer
    queryset = Events.objects.all()

    def perform_create(self, serializer):
        """ Create a new event"""
        serializer.save(editor=self.request.user)


class LocationViewSet(viewsets.ModelViewSet):
    """ Manage events in the database """
    serializer_class = serializers.LocationSerializer
    queryset = Location.objects.all()
