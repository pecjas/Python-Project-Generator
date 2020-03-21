import os
from distutils.util import strtobool

FILE_CONTENTS = {
    "main": {
        "__init__.py": [],
        "main.py": [
            'import <app_name>.<app_name>',
            '',
            'if __name__ == "__main__":',
            '\t<app_name>.start_application()',
            ''
        ],

        "LICENSE": [], #TODO
        ".gitignore": [], #TODO

        "Run Application.lnk": [], #TODO
        "Run Unit Tests.lnk": [] #TODO
    },

    "test": {
        "__init__.py": [],
        "test_<app_name>.py": [
            'import unittest',
            '',
            'class ApplicationTests(unittest.TestCase):',
            '',
            '\tdef setUp(self):',
            '\t\tpass',
            '',
            '\tdef tearDown(self):',
            '\t\tpass',
            '',
            '\tdef test_case_one(self):',
            '\t\tself.assertTrue(True)',
            ''
            'if __name__ == "__main__":',
            '\tunittest.main()',
            ''
        ]
    },

    "app": {
        "__init__.py": [],
        "<app_name>.py": [
            'def start_application():',
            '\tpass',
            ''
        ]
    },

    "placeholder": "<app_name>"
}

class ProjectParameters():

    def __init__(self):
        self.app_name = None
        self.starting_directory = None

    def prompt_for_project_parameters(self):

        app_name = self.app_name
        while app_name is None:
            app_name = input("What should be the name of the new app?: ")
            app_name = remove_whitespace(app_name)

        starting_directory = self.starting_directory
        while starting_directory is None:
            starting_directory = input("Enter the full path of the starting directory for the new project: ")
            #TODO: Add path validation

        self.app_name = app_name
        self.starting_directory = starting_directory        

    def validate_parameters(self) -> bool:
        print("The new application will be created using the following parameters.")

        print(f"\tApp Name: {self.app_name}")
        print(f"\tStarting Directory: {self.starting_directory}")

        return strtobool(input("Continue?"))
def make_testable_application():
    project_params = ProjectParameters()
    project_params.prompt_for_project_parameters()
    if not project_params.validate_parameters():
        wait_for_exit("Inputs not confirmed. Press any key to quit.")

    else:
        os.chdir(fr"{project_params.starting_directory}")

        base_directory = os.path.join(project_params.starting_directory, project_params.app_name)
        os.mkdir(base_directory)

        os.chdir(base_directory)
        make_base_directory_files(base_directory)

        test_directory = os.path.join(base_directory, "test")
        os.mkdir(test_directory)

        os.chdir(test_directory)
        make_test_directory_files(test_directory, project_params.app_name)

        os.chdir(base_directory)
        app_directory = os.path.join(base_directory, project_params.app_name)
        os.mkdir(app_directory)

        os.chdir(app_directory)
        make_app_directory_files(app_directory, project_params.app_name)
        wait_for_exit("The app template has been created. Press any key to exit.")

def remove_whitespace(value: str) -> str:
    value = value.split()
    return '_'.join(value)

def make_base_directory_files(directory: str):
    create_file_in_directory("LICENSE", directory, []) #TODO: License contents
    create_file_in_directory(".gitignore", directory, []) #TODO: .gitignore contents

    create_file_in_directory("__init__.py", directory, [])
    create_file_in_directory("main.py", directory, []) #TODO: main.py contents

    create_file_in_directory("Run Application.lnk", directory, []) #TODO: Contents
    create_file_in_directory("Run Unit Tests.lnk", directory, []) #TODO: Contents

def create_file_in_directory(file_name: str, directory: str, contents: list):
    init_file = open(os.path.join(directory, file_name), "w")

    if len(contents) > 0:
        init_file.writelines(contents)

    init_file.close()

def make_test_directory_files(directory: str, app_name: str):
    create_file_in_directory("__init__.py", directory, [])
    create_file_in_directory(f"test_{app_name}.py", directory, []) #TODO: contents

def make_app_directory_files(directory: str, app_name: str):
    create_file_in_directory("__init__.py", directory, [])
    create_file_in_directory(f"{app_name}.py", directory, []) #TODO: contents

def wait_for_exit(prompt: str):
    input(prompt)

if __name__ == "__main__":
    make_testable_application()
