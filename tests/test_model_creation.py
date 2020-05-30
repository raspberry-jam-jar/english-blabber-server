from django.test import TestCase

from tests.data_factories import UserFactory


class UserCreationTestCase(TestCase):
    def test_student_creation(self):
        student = UserFactory(role='student')
        self.assertTrue(student.hero,
                        'Student should have at least the base hero after creation')
