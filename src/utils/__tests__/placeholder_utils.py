import unittest

from src.utils import placeholder_utils
from src.utils.__tests__.test_constants import ESSAY_WITHOUT_PLACEHOLDERS, ESSAY_WITH_PLACEHOLDERS_1, \
    ESSAY_WITH_PLACEHOLDERS_2, ESSAY_WITH_PLACEHOLDERS_3, ESSAY_WITH_SUBBED_PLACEHOLDERS_1, \
    ESSAY_WITH_SUBBED_PLACEHOLDERS_3, EXPECTED_PRINT_STATEMENTS, STATIC_PLACEHOLDER_DICT
from ..placeholder_utils import get_all_placeholders, get_missing_placeholders, parse_placeholder, \
    provide_missing_placeholders, request_missing_placeholders, sub_placeholder, \
    sub_placeholders_in_essays

from unittest.mock import patch


def assert_stdout(value, expected_value):
    assert value == expected_value


class TestPlaceholderUtils(unittest.TestCase):

    def test_parse_simple_placeholder(self):
        placeholder_name = "[Your name]"
        self.assertEqual(parse_placeholder(placeholder_name), ["yourname"])

    def test_parse_placeholder_with_special_characters(self):
        placeholder_name = "[Senator's name, ZIP code]"
        self.assertEqual(parse_placeholder(placeholder_name), ["senatname", "zipcode"])

    def test_parse_placeholder_with_numbers(self):
        placeholder_name = "[Source 1]"
        self.assertEqual(parse_placeholder(placeholder_name), ["sourc1"])

    def test_get_all_placeholders(self):
        responses = [ESSAY_WITH_PLACEHOLDERS_1, ESSAY_WITH_PLACEHOLDERS_2, ESSAY_WITHOUT_PLACEHOLDERS]
        expected_placeholders = ['placehold1', 'yourname', 'adject', 'companiname', 'streetname']
        actual_placeholders = get_all_placeholders(responses)
        self.assertEqual(sorted(expected_placeholders), sorted(actual_placeholders))

    def test_get_all_placeholders_with_duplicates(self):
        responses = [ESSAY_WITH_PLACEHOLDERS_2, ESSAY_WITH_PLACEHOLDERS_2, ESSAY_WITHOUT_PLACEHOLDERS]
        expected_placeholders = ['adject', 'companiname', 'streetname']
        actual_placeholders = get_all_placeholders(responses)
        self.assertEqual(sorted(expected_placeholders), sorted(actual_placeholders))
        self.assertEqual(len(expected_placeholders), len(actual_placeholders))

    def test_sub_placeholders_single_placeholder(self):
        placeholder_name = '[Your name]'
        expected_string = 'Alicia Keys'
        actual_string = sub_placeholder(placeholder_name, STATIC_PLACEHOLDER_DICT)

        self.assertEqual(expected_string, actual_string)

    def test_sub_placeholders_multiple_placeholders(self):
        placeholder_name = '[Your name, Adjective]'
        expected_string = 'Alicia Keys, bombastic'
        actual_string = sub_placeholder(placeholder_name, STATIC_PLACEHOLDER_DICT)

        self.assertEqual(expected_string, actual_string)

    def test_sub_placeholders_with_missing_keys(self):
        placeholder_name = '[Your name, Missing Placeholder, Adjective]'
        expected_string = 'Alicia Keys, [missplacehold], bombastic'
        actual_string = sub_placeholder(placeholder_name, STATIC_PLACEHOLDER_DICT)

        self.assertEqual(expected_string, actual_string)

    @patch.object(placeholder_utils, 'get_placeholder_dict')
    def test_sub_placeholders_in_essays(self, mock_get_placeholder_dict):
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        essays = [ESSAY_WITH_PLACEHOLDERS_1]
        expected_result = [ESSAY_WITH_SUBBED_PLACEHOLDERS_1]
        actual_result = sub_placeholders_in_essays(essays, {})
        self.assertEqual(expected_result, actual_result)

    @patch.object(placeholder_utils, 'get_placeholder_dict')
    def test_sub_placeholders_in_essay_missing_values(self, mock_get_placeholder_dict):
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        essays = [ESSAY_WITH_PLACEHOLDERS_3]
        expected_result = [ESSAY_WITH_SUBBED_PLACEHOLDERS_3]
        actual_result = sub_placeholders_in_essays(essays, {})
        self.assertEqual(expected_result, actual_result)

    @patch.object(placeholder_utils, 'get_placeholder_dict')
    def test_get_missing_placeholders(self, mock_get_placeholder_dict):
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        essays = [ESSAY_WITH_SUBBED_PLACEHOLDERS_1, ESSAY_WITH_PLACEHOLDERS_3]
        expected_result = {"missplacehold"}
        actual_result = get_missing_placeholders(essays)

        self.assertEqual(expected_result, actual_result)

    @patch.object(placeholder_utils, 'get_placeholder_dict')
    def test_get_missing_placeholders_with_no_placeholder_missing(self, mock_get_placeholder_dict):
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        essays = [ESSAY_WITH_SUBBED_PLACEHOLDERS_1, ESSAY_WITH_PLACEHOLDERS_2]
        expected_result = set()
        actual_result = get_missing_placeholders(essays)

        self.assertEqual(expected_result, actual_result)

    @patch.object(placeholder_utils, 'get_missing_placeholders')
    @patch.object(placeholder_utils, 'get_placeholder_dict')
    @patch.object(placeholder_utils, 'request_missing_placeholders')
    def test_provide_missing_placeholders(self, mock_request_missing_placeholders, mock_get_placeholder_dict,
                                          mock_get_missing_placeholders):
        mock_request_missing_placeholders.return_value = {'missplacehold': 'Cool Missing Placeholder'}
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        mock_get_missing_placeholders.return_value = {"missplacehold"}

        essays = [
            ESSAY_WITH_SUBBED_PLACEHOLDERS_1,
            ESSAY_WITH_PLACEHOLDERS_3,
            ESSAY_WITH_PLACEHOLDERS_2,
            ESSAY_WITHOUT_PLACEHOLDERS
        ]

        expected_result = {'missplacehold': 'Cool Missing Placeholder'}
        actual_result = provide_missing_placeholders(essays)

        self.assertEqual(expected_result, actual_result)

    @patch.object(placeholder_utils, 'get_missing_placeholders')
    @patch.object(placeholder_utils, 'get_placeholder_dict')
    @patch.object(placeholder_utils, 'request_missing_placeholders')
    def test_provide_missing_placeholders_with_no_placeholder_missing(self, mock_request_missing_placeholders,
                                                                      mock_get_placeholder_dict,
                                                                      mock_get_missing_placeholders):
        mock_request_missing_placeholders.return_value = {}
        mock_get_placeholder_dict.return_value = STATIC_PLACEHOLDER_DICT
        mock_get_missing_placeholders.return_value = set()

        essays = [
            ESSAY_WITH_SUBBED_PLACEHOLDERS_1,
            ESSAY_WITH_PLACEHOLDERS_2,
            ESSAY_WITHOUT_PLACEHOLDERS
        ]

        expected_result = {}
        actual_result = provide_missing_placeholders(essays)

        self.assertEqual(expected_result, actual_result)

    def test_request_missing_placeholders(self):
        with patch('src.utils.placeholder_utils.input',
                   side_effect=["y", "Placeholder 1 Value", "Placeholder 2 Value"]):
            missing_placeholders = sorted({"placeholder1", "placeholder2"})

            expected_result = {"placeholder1": "Placeholder 1 Value", "placeholder2": "Placeholder 2 Value"}
            actual_result = request_missing_placeholders(missing_placeholders)

            self.assertEqual(expected_result, actual_result)

    def test_request_missing_placeholders_user_rejection(self):
        with patch('src.utils.placeholder_utils.input', side_effect=["n"]):
            missing_placeholders = sorted({"placeholder1", "placeholder2"})

            expected_result = {}
            actual_result = request_missing_placeholders(missing_placeholders)

            self.assertEqual(expected_result, actual_result)

    def test_request_missing_placeholders_invalid_response(self):

        print_statements = EXPECTED_PRINT_STATEMENTS

        with patch(
                'src.utils.placeholder_utils.input',
                side_effect=["mmm", "y", "Placeholder 1 Value", "Placeholder 2 Value"]):
            with patch(
                    'src.utils.placeholder_utils.print',
                    side_effect=lambda value: assert_stdout(value, print_statements.pop(0))
            ):

                missing_placeholders = sorted({"placeholder1", "placeholder2"})

                expected_result = {"placeholder1": "Placeholder 1 Value", "placeholder2": "Placeholder 2 Value"}
                actual_result = request_missing_placeholders(missing_placeholders)

                self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
