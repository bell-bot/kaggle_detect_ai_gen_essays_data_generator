import unittest
from unittest.mock import MagicMock, Mock, patch

from faker import Faker
from src.utils import placeholder_dict
from src.utils.placeholder_dict import get_placeholder_dict


class TestPlaceholderDict(unittest.TestCase):

    def test_get_placeholder_dict_with_additional_values(self):
        additional_items = {
            'item1': 'Item 1',
            'item2': 'Item 2'
        }

        placeholder_dict = get_placeholder_dict(additional_items)

        for item in additional_items.items():

            self.assertTrue(item in placeholder_dict.items())

    @patch.object(placeholder_dict, "fake")
    def test_get_placeholder_dict_with_additional_values_containing_refs(self, mock_faker):

        mock_faker.last_name.side_effect = ["Pip", "Pippin", "Mortal", "Combat"]
        mock_faker.first_name.return_value = "Minnie"

        additional_items = {
           'item1': 'fake.last_name()',
           'item2': 'your_first_name fake.last_name()'
        }

        test_placeholder_dict = get_placeholder_dict(additional_items)
        self.assertEqual('Mortal', test_placeholder_dict['item1'])
        self.assertEqual(f"{test_placeholder_dict['firstname']} Combat", test_placeholder_dict['item2'])
