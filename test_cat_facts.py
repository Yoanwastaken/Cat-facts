import unittest
from unittest.mock import patch, Mock
import requests

# Import functions from cat_facts.py
from catFacts import (
    get_single_fact,
    create_mock_fact,
    update_mock_fact,
    delete_mock_fact
)


class TestCatFactsAPI(unittest.TestCase):

    @patch("requests.get")
    def test_get_single_fact_success(self, mock_get):
        """Test fetching a single cat fact successfully."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"fact": "Cats sleep 16 hours a day."}
        mock_get.return_value = mock_response

        with patch("builtins.print") as mocked_print:
            get_single_fact()
            mocked_print.assert_called_with("Cat Fact:", "Cats sleep 16 hours a day.")

    @patch("requests.get")
    def test_get_single_fact_failure(self, mock_get):
        """Test handling API failure during GET request."""
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        with patch("builtins.print") as mocked_print:
            get_single_fact()
            mocked_print.assert_called_with("Error in GET request:", "API Error")

    @patch("requests.post")
    def test_create_mock_fact_success(self, mock_post):
        """Test simulating the creation of a fact (POST)."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"fact": "Cats love laser pointers.", "type": "cat_fact"}
        mock_post.return_value = mock_response

        with patch("builtins.print") as mocked_print:
            create_mock_fact({"fact": "Cats love laser pointers."})
            mocked_print.assert_called_with("POST Response:", mock_response.json())

    @patch("requests.post")
    def test_create_mock_fact_failure(self, mock_post):
        """Test handling API failure during POST request."""
        mock_post.side_effect = requests.exceptions.RequestException("POST Error")

        with patch("builtins.print") as mocked_print:
            create_mock_fact({"fact": "Cats love boxes."})
            mocked_print.assert_called_with("Error in POST request:", "POST Error")

    @patch("requests.put")
    def test_update_mock_fact_failure(self, mock_put):
        """Test handling API failure during PUT request."""
        mock_put.side_effect = requests.exceptions.RequestException("PUT Error")

        with patch("builtins.print") as mocked_print:
            update_mock_fact("123", {"fact": "Updated fact."})
            mocked_print.assert_called_with("Error in PUT request:", "PUT Error")

    @patch("requests.delete")
    def test_delete_mock_fact_failure(self, mock_delete):
        """Test handling API failure during DELETE request."""
        mock_delete.side_effect = requests.exceptions.RequestException("DELETE Error")

        with patch("builtins.print") as mocked_print:
            delete_mock_fact("123")
            mocked_print.assert_called_with("Error in DELETE request:", "DELETE Error")


if __name__ == "__main__":
    unittest.main()
