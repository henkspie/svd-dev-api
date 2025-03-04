"""
URL mappings for the famTree app.
"""

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from famTree import views


router = DefaultRouter()
router.register("members", views.MemberViewSet)
router.register("events", views.EventViewSet)
router.register("location", views.LocationViewSet)
# router.register("ingredients", views.IngredientViewSet)

app_name = "famTree"

urlpatterns = [
    path("", include(router.urls)),
]
