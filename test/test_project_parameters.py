import unittest
from unittest.mock import patch
from python_project_generator.project_parameters import ProjectParameters

ACCEPT_VALUES = ['y', 'yes', 't', 'true', 'on', '1']
DECLINE_VALUES = ['n', 'no', 'f', 'false', 'off', '0']
UNKNOWN_VALUES = ['what', 'Nah', 'yepper', ';', '!$']

class ProjectParametersTests(unittest.TestCase):

    def setUp(self):
        self.params = ProjectParameters()

    def tearDown(self):
        pass

    def test_set_start_directory(self):
        self._set_named_directory_helper("start")

    def test_set_base_directory(self):
        self._set_named_directory_helper("base")

    def _set_named_directory_helper(self, directory_name: str):
        directory = r"C:\Users\pecja\Desktop\test123\dfah_asdf"
        other_named_directory = "base" if directory_name == "start" else "start"

        self.params.set_named_directory(directory_name, directory)

        self.assertEqual(directory, self.params.directories.get(directory_name))
        self.assertEqual(
            self.params.directories.get(other_named_directory),
            ProjectParameters.directory_default)
        self.assertEqual(len(self.params.directories.get("others")), 0)


    def test_get_directory_or_default_start(self):
        self._get_directory_or_default_helper("start")

    def test_get_directory_or_default_base(self):
        self._get_directory_or_default_helper("base")

    def _get_directory_or_default_helper(self, directory_name: str):
        self.params.directories.update({directory_name: ProjectParameters.directory_default})
        self.assertEqual(self.params.get_directory_or_default(directory_name), "")

        directory = r"C:\Users\pecja\Desktop"
        self.params.directories.update({directory_name: directory})
        self.assertEqual(self.params.get_directory_or_default(directory_name), directory)

    def test_get_directory_or_default_other(self):
        directory_name = "test123"
        directory = r"C:\Users\pecja\Documents"

        self.params.directories["others"].clear()
        self.assertEqual(self.params.get_directory_or_default(directory_name), "")

        self.params.directories["others"].update({directory_name: directory})
        self.assertEqual(self.params.get_directory_or_default(directory_name), directory)


    def test_remove_whitespace(self):
        initial_values = {
            1: "Text with spaces",
            2: "Textwithoutspaces",
            3: "Mixed    spac1ng distance",
            4: "dsfa54549%&&( af",
            5: "test _with some_ underscores"
        }

        expected_outputs = {
            1: "Text_with_spaces",
            2: "Textwithoutspaces",
            3: "Mixed_spac1ng_distance",
            4: "dsfa54549%&&(_af",
            5: "test__with_some__underscores"
        }

        for key in initial_values:
            self.assertEqual(
                ProjectParameters.remove_whitespace(initial_values.get(key)),
                expected_outputs.get(key)
            )


    @patch('builtins.input', side_effect=ACCEPT_VALUES)
    def test_validate_parameters_accept(self, mock_inputs: list):
        for value in ACCEPT_VALUES:
            result = self.params.validate_parameters(value)

            self.assertTrue(result)

    @patch('builtins.input', side_effect=DECLINE_VALUES)
    def test_validate_parameters_decline(self, mock_inputs: list):
        for value in DECLINE_VALUES:
            result = self.params.validate_parameters(value)

            self.assertFalse(result)

    @patch('builtins.input', side_effect=UNKNOWN_VALUES)
    def test_validate_parameters_unknown(self, mock_inputs: list):
        for value in UNKNOWN_VALUES:
            result = self.params.validate_parameters(value)

            self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
