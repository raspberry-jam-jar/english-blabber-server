from rest_framework import views, viewsets, status
from rest_framework.response import Response
from django.utils import timezone

import class_room.serializers as ser
import helpers as help
from .models import SocialUser


class SocialUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    queryset = SocialUser
    serializer_class = ser.CreateSocialUserSerializer


class VkSocialUserAuth(views.APIView):
    def get(self,  request, *args, **kwargs):
        code = request.GET.get('vk_user_id')
        if not help.is_vk_signature_valid(query=request.GET.dict()) or \
                code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                social_user = SocialUser.objects.get(code=code)
            except SocialUser.DoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)

            if not social_user.user:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            social_user.datetime_last_edited = timezone.now()
            social_user.save()

            return Response(
                data={'password': help.generate_signature(social_user)}
            )
