from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health(_request):
    return Response({"status": "ok", "service": "HarmonySphere API", "version": "1.0.0"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health),
    path("v1/", include("music_api.urls")),
]
