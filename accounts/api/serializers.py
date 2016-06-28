from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    CharField,
    )

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        ]
        extra_kwargs = {"password":
                        {"write_only":True}
                }
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        user_obj = User(
            username=username,
            email=email
            )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank = True, read_only=True)
    username = CharField()
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                        {"write_only":True}
                }
    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data['password']
        if not username:
            raise ValidationError("A username is requitred to login.")
        user_obj = User.objects.filter(username = username)
        if user_obj.exists() and user_obj.count() == 1:
            user_obj = user_obj.first()
        else:
            raise ValidationError("This username is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect Credentials.")
        data['token'] = "SOME RANDOM TOKEN"
        return data
