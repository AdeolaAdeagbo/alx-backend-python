#!/usr/bin/env python3
"""Unit tests for utils module"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
import utils
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),  # empty dict, key missing
        ({"a": 1}, ("a", "b")),  # nested key missing
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised for invalid paths"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Ensure the error message matches the missing key
        expected_message = repr(path[-1])
        self.assertEqual(str(cm.exception), expected_message)


class TestGetJson(unittest.TestCase):
    """Test case for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns expected result with mocked requests.get"""
        with patch("utils.requests.get") as mock_get:
            # Configure mock response
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call function
            result = utils.get_json(test_url)

            # Assertions
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoization decorator"""

    def test_memoize(self):
        """Test that memoize caches results properly"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call the memoized property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Both calls should return same result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # But a_method should only be called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

