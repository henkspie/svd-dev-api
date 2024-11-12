"""
Views for the svdUser API.
"""
from rest_framework import generics

from svdUser.serializers import SvdUserSerializer


class CreateSvdUserView(generics.CreateAPIView):
    """ Create a new svdUser in the system"""
    serializer_class = SvdUserSerializer