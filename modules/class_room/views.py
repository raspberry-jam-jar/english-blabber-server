from rest_framework import views, viewsets
from rest_framework.response import Response

import class_room.serializers as ser
from .models import SocialUser


class SocialUserStatusView(views.APIView):
    def get(self, request, code, *args, **kwargs):
        status_id = None
        try:
            social_user = SocialUser.objects.get(code=code)
        except SocialUser.DoesNotExist:
            status_id = 'new'
        else:
            status_id = 'user' if social_user.user else 'pending'
        finally:
            return Response(data={'status': status_id})


class SocialUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    queryset = SocialUser
    serializer_class = ser.CreateSocialUserSerializer
