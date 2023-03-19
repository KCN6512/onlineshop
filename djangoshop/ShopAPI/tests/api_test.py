from django.test import TestCase


class APITestCase(TestCase):
    def test_equal(self):
        a = 2 * 2
        self.assertEqual(a, 5)
