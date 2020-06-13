from django.views.decorators.csrf import ensure_csrf_cookie
from django import http
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone

import class_room.serializers as ser
import helpers as help
from .models import SocialUser


class SocialUserViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', ]
    queryset = SocialUser
    serializer_class = ser.CreateSocialUserSerializer

    def create(self, request, *args, **kwargs):
        try:
            SocialUser.objects.get(
                code=request.data['code'],
                platform=request.data.get('platform', 'vk')
            )
        except SocialUser.DoesNotExist:
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_200_OK)


class HttpResponseUnauthorized(http.HttpResponse):
    status_code = 401


@ensure_csrf_cookie
def vk_social_user_auth(request, *args, **kwargs):
    if not request.method == 'GET':
        return http.HttpResponseNotAllowed(['GET'])
    code = request.GET.get('vk_user_id')
    if not help.is_vk_signature_valid(query=request.GET.dict()) or \
            code is None:
        return http.HttpResponseBadRequest()
    else:
        try:
            social_user = SocialUser.objects.get(code=code)
        except SocialUser.DoesNotExist:
            return http.HttpResponseForbidden()

        if not social_user.user:
            return HttpResponseUnauthorized()

        social_user.datetime_last_edited = timezone.now()
        social_user.save()

        return http.JsonResponse(
            data={'password': help.generate_signature(social_user)}
        )
