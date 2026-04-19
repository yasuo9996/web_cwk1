from rest_framework import serializers

from .models import ListeningRecord, Track


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class SimilarTrackSerializer(serializers.Serializer):
    track_id = serializers.IntegerField()
    similarity = serializers.FloatField()


class ListeningRecordCreateSerializer(serializers.ModelSerializer):
    track_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ListeningRecord
        fields = ["id", "user_id", "track_id", "action_type", "listened_at"]
        read_only_fields = ["id", "listened_at"]

    def create(self, validated_data):
        track_id = validated_data.pop("track_id")
        track = Track.objects.filter(id=track_id).first()
        if track is None:
            raise serializers.ValidationError({"track_id": "Track not found"})
        return ListeningRecord.objects.create(track=track, **validated_data)


class ListeningRecordSerializer(serializers.ModelSerializer):
    track_id = serializers.IntegerField(source="track.id", read_only=True)

    class Meta:
        model = ListeningRecord
        fields = ["id", "user_id", "track_id", "action_type", "listened_at"]


class ListeningRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningRecord
        fields = ["action_type"]


class UserInsightsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    preferred_energy_range = serializers.ListField(child=serializers.FloatField(), allow_null=True)
    preferred_danceability_range = serializers.ListField(child=serializers.FloatField(), allow_null=True)
    avg_tempo = serializers.FloatField(allow_null=True)
    total_records = serializers.IntegerField()


class HistogramBinSerializer(serializers.Serializer):
    range_start = serializers.FloatField()
    range_end = serializers.FloatField()
    count = serializers.IntegerField()


class FeatureDistributionSerializer(serializers.Serializer):
    feature = serializers.CharField()
    bins = HistogramBinSerializer(many=True)
