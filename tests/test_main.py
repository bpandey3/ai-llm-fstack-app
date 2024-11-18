import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from dataclasses import dataclass

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import process, create_list_items

# Create a mock Summary class to simulate the response from ice_break_with
@dataclass
class MockSummary:
    summary: str
    facts: list

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts
        }

class TestMain(unittest.TestCase):
    def setUp(self):
        # Setup common test data
        self.test_name = "John Doe"
        self.test_summary = "Test summary"
        self.test_facts = ["Fact 1", "Fact 2"]
        self.test_profile_pic = "http://example.com/pic.jpg"
        
        # Create mock summary object
        self.mock_summary = MockSummary(
            summary=self.test_summary,
            facts=self.test_facts
        )

    @patch('main.ice_break_with')
    def test_process_successful(self, mock_ice_break):
        # Configure the mock
        mock_ice_break.return_value = (self.mock_summary, self.test_profile_pic)

        # Call the process function
        result = process(self.test_name)

        # Assert ice_break_with was called with correct parameters
        mock_ice_break.assert_called_once_with(name=self.test_name)

        # Assert the result structure and content
        expected_result = {
            "summary_and_facts": {
                "summary": self.test_summary,
                "facts": self.test_facts
            },
            "picture_url": self.test_profile_pic
        }
        self.assertEqual(result, expected_result)

    @patch('main.ice_break_with')
    def test_process_with_error(self, mock_ice_break):
        # Configure the mock to raise an exception
        mock_ice_break.side_effect = Exception("API Error")

        # Assert that the function raises the exception
        with self.assertRaises(Exception) as context:
            process(self.test_name)
        
        self.assertTrue("API Error" in str(context.exception))

    @patch('main.st')
    def test_create_list_items(self, mock_st):
        # Test data
        test_items = ["Item 1", "Item 2", "Item 3"]
        
        # Call the function
        create_list_items(test_items)

        # Assert markdown was called for each item
        self.assertEqual(mock_st.markdown.call_count, len(test_items))
        
        # Assert the format of each markdown call
        expected_calls = [unittest.mock.call(f"- {item}") for item in test_items]
        mock_st.markdown.assert_has_calls(expected_calls)

    @patch('main.st')
    def test_create_list_items_empty_list(self, mock_st):
        # Test with empty list
        create_list_items([])
        
        # Assert markdown was not called
        mock_st.markdown.assert_not_called()

    @patch('main.st')
    def test_create_list_items_none(self, mock_st):
        # Test with None
        create_list_items(None)
        
        # Assert markdown was not called
        mock_st.markdown.assert_not_called()

if __name__ == '__main__':
    unittest.main() 