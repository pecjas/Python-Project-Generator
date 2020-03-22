import unittest
from python_project_generator.create_contents import (PLACEHOLDER, replace_app_with_placeholder, replace_placeholders_in_string)

class CreateContentsTests(unittest.TestCase):
    app = "APP"
    user = "USER"

    app_placeholder = PLACEHOLDER.get('app')
    user_placeholder = PLACEHOLDER.get('github')

    strings_with_app_placeholder = {
        1: f'What a cool {app_placeholder}',
        2: f"{app_placeholder}'s are fun",
        3: f'{app_placeholder}{app_placeholder}{app_placeholder}',
        4: f'{app_placeholder} is {app_placeholder}',
        5: f"Nothing to replace here."
    }

    strings_with_app_populated = {
        1: f'What a cool {app}',
        2: f"{app}'s are fun",
        3: f'{app}{app}{app}',
        4: f'{app} is {app}',
        5: f"Nothing to replace here."
    }

    strings_with_mixed_placeholders = {
        1: f"{app_placeholder} is made by {user_placeholder}",
        2: f"This user, {user_placeholder}, created {app_placeholder}",
        3: f"{app_placeholder}{app_placeholder}{user_placeholder}",
        4: f"{user_placeholder}'''{app_placeholder}'''{user_placeholder}",
        5: f"Nothing to replace here."
    }

    strings_with_mixed_populated = {
        1: f"{app} is made by {user}",
        2: f"This user, {user}, created {app}",
        3: f"{app}{app}{user}",
        4: f"{user}'''{app}'''{user}",
        5: f"Nothing to replace here."
    }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_replace_app_with_placeholder(self):
        for key, value in CreateContentsTests.strings_with_app_populated.items():

            self.assertEqual(
                replace_app_with_placeholder(value, CreateContentsTests.app),
                CreateContentsTests.strings_with_app_placeholder.get(key))

    def test_replace_placeholders_in_string(self):
        project_params = MockProjectParameters(
            CreateContentsTests.app,
            CreateContentsTests.user)

        for key, value in CreateContentsTests.strings_with_mixed_placeholders.items():

            self.assertEqual(
                replace_placeholders_in_string(value, project_params),
                CreateContentsTests.strings_with_mixed_populated.get(key))

class MockProjectParameters():
    def __init__(self, app: str, user: str):
        self.app_name = app
        self.user = user

if __name__ == "__main__":
    unittest.main()
