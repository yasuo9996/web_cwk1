from django.contrib import admin

from .models import ListeningRecord, Track, UserProfile

admin.site.register(Track)
admin.site.register(UserProfile)
admin.site.register(ListeningRecord)
