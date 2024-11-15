"""
URL mappings for the user API.
"""
from django.urls import path

from svdUser import views


app_name = 'svdUser'

urlpatterns = [
    path('create/', views.CreateSvdUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
]
