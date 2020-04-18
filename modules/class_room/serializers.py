from rest_framework.serializers import ModelSerializer

from .models import SocialUser


class CreateSocialUserSerializer(ModelSerializer):
    class Meta:
        model = SocialUser
        fields = ('code', 'platform', 'first_name', 'last_name')
