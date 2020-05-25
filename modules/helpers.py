from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from urllib.parse import urlencode

from django.conf import settings


def _generate_decoded_hash_code(*, secret: str, subset: OrderedDict) -> str:
    hash_code = b64encode(
        HMAC(
            secret.encode(), urlencode(subset, doseq=True).encode(), sha256
        ).digest()
    )
    return hash_code.decode('utf-8')[:-1].replace('+', '-').replace('/', '_')


def is_vk_signature_valid(*, query: dict) -> bool:
    vk_subset = OrderedDict(
        sorted(x for x in query.items() if x[0][:3] == "vk_")
    )
    decoded_hash_code = _generate_decoded_hash_code(
        secret=settings.VK_CLIENT_SECRET, subset=vk_subset
    )

    return query["sign"] == decoded_hash_code


def generate_signature(social_user) -> str:
    """
    Generate signature for social user payload.

    :param social_user: SocialUser model instance
    :return: signature
    """

    social_subset = social_user.payload

    return _generate_decoded_hash_code(
        secret=settings.SECRET_KEY, subset=social_subset
    )


def validate_signature(signature: str, social_user) -> bool:
    """
    Validate signature for social user.

    :param signature: string
    :param social_user: SocialUser model instance
    :return: boolean is signature valid for passed social user
    """

    return signature == generate_signature(social_user)
