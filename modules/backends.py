from class_room.models import SocialUser
from helpers import validate_signature


class RemoteSocialUserBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate remote social user if the user is associated
        with system user.

        :param request:
        :param username: social user id code
        :param password: social user signature
        :param kwargs:
        :return: None or user instance
        """

        try:
            social_user = SocialUser.objects.get(code=username)
        except SocialUser.DoesNotExist:
            return None

        signature_valid = validate_signature(password, social_user)
        if signature_valid:
            return social_user.user
        return None
