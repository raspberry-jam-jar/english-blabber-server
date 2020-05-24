from django.test import TestCase
from django.utils import timezone

from tests.data_factories import SocialUserFactory
from helpers import generate_signature, validate_signature


class SignatureTestCase(TestCase):
    def test_valid_signature_for_matched_user(self):
        any_code = '1Ab56'
        any_social_user = SocialUserFactory(
            code=any_code, datetime_last_edited=timezone.now()
        )

        first_time_generated_signature = generate_signature(any_social_user)

        self.assertTrue(
            validate_signature(first_time_generated_signature, any_social_user)
        )

        any_social_user.datetime_last_edited = timezone.now()
        any_social_user.save()

        second_time_generated_signature = generate_signature(any_social_user)

        self.assertFalse(
            validate_signature(first_time_generated_signature, any_social_user)
        )
        self.assertTrue(
            validate_signature(second_time_generated_signature, any_social_user)
        )

    def test_valid_signature_for_unmatched_user(self):
        any_code = '1Ab56'
        any_social_user = SocialUserFactory(
            code=any_code, datetime_last_edited=timezone.now()
        )

        other_code = 'Q5d091'
        other_social_user = SocialUserFactory(
            code=other_code, datetime_last_edited=timezone.now()
        )

        first_time_generated_signature = generate_signature(any_social_user)

        self.assertFalse(
            validate_signature(first_time_generated_signature, other_social_user)
        )
