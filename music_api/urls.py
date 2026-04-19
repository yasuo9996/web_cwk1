from django.urls import path

from . import views

urlpatterns = [
    path("", views.home),
    path("tracks/features/<int:track_id>", views.get_track_features),
    path("tracks/similar", views.get_similar_tracks),
    path("listening/log", views.create_listening_log),
    path("listening", views.list_listening_logs),
    path("listening/<int:record_id>", views.listening_record_detail),
    path("profile/<int:user_id>/insights", views.get_user_insights),
    path("analytics/feature-distribution", views.get_feature_distribution),
]
