from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField, SerializerMethodField
from chirps.models import Chirp

class ChirpListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name="chirps-api:detail")
    delete_url = HyperlinkedIdentityField(view_name="chirps-api:delete")
    user = SerializerMethodField()
    class Meta:
        model = Chirp
        fields = [
            'url',
            'user',
            'id',
            'content',
            'timestamp',
            'delete_url',
        ]
    def get_user(self, obj):
        return str(obj.user.username)

class ChirpCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Chirp
        fields = [
            'content',
        ]

class ChirpDetailSerializer(ModelSerializer):
    class Meta:
        model = Chirp
        fields = [
            'content',
            'timestamp',
            'rechirp_status',
        ]
