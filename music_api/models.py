from django.db import models


class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    danceability = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    loudness = models.FloatField(null=True, blank=True)
    valence = models.FloatField(default=0.0)
    acousticness = models.FloatField(default=0.0)
    tempo = models.FloatField(null=True, blank=True)


class UserProfile(models.Model):
    user_id = models.IntegerField(unique=True)
    preferred_energy_min = models.FloatField(null=True, blank=True)
    preferred_energy_max = models.FloatField(null=True, blank=True)
    preferred_danceability_min = models.FloatField(null=True, blank=True)
    preferred_danceability_max = models.FloatField(null=True, blank=True)
    avg_tempo = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class ListeningRecord(models.Model):
    ACTION_CHOICES = (
        ("listen", "listen"),
        ("like", "like"),
        ("skip", "skip"),
    )

    user_id = models.IntegerField(db_index=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="listening_records")
    listened_at = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
