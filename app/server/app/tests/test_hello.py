from django.test import TestCase

class HelloWorld(TestCase):
    def test_helloworld(self):
        self.assertEqual(1, 2)