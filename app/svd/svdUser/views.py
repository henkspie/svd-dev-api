"""
Views for the svdUser API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from svdUser.serializers import (
    SvdUserSerializer,
    AuthTokenSerializer,
)


class CreateSvdUserView(generics.CreateAPIView):
    """ Create a new svdUser in the system"""
    serializer_class = SvdUserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for svdUser."""
    serializer_class = AuthTokenSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES