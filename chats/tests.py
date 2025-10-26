from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic(self):
        """Basic test to verify testing works"""
        self.assertEqual(1 + 1, 2)
    
    def test_string(self):
        """Test string operations"""
        self.assertEqual("hello".upper(), "HELLO")
