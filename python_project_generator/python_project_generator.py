import os
import sys
from distutils.util import strtobool
import winshell

PROJECT_CONTENTS = {
    "base": {
        "__init__.py": [],
        "main.py": [
            'from <app_name>.<app_name> import start_application\n',
            '\n',
            'if __name__ == "__main__":\n',
            '    start_application()\n',
        ],

        "LICENSE": [ #Defaults to MIT
            'MIT License\n',
            '\n'
            'Copyright (c) 2019 pecjas\n' #TODO: replace username
            'Permission is hereby granted, free of charge, to any person obtaining a copy\n'
            'of this software and associated documentation files (the "Software"), to deal\n'
            'in the Software without restriction, including without limitation the rights\n'
            'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n'
            'copies of the Software, and to permit persons to whom the Software is\n'
            'furnished to do so, subject to the following conditions:\n'
            '\n'
            'The above copyright notice and this permission notice shall be included in all\n'
            'copies or substantial portions of the Software.\n'
            '\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n'
            'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n'
            'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n'
            'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n'
            'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n'
            'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n'
            'SOFTWARE.\n'
        ],
        ".gitignore": [
            '__pycache__\n',
            '*.lnk\n',
            '.vscode/\n'
        ],

        "Run Application.lnk": {
            "path": r'C:\Windows\System32\cmd.exe',
            "target": r"C:\Windows\System32\cmd.exe",
            "arguments": '"/c" python main.py',
            "description": "Run Application"
        },
        "Run Unit Tests.lnk": {
            "path": r'C:\Windows\System32\cmd.exe',
            "target": r"C:\Windows\System32\cmd.exe",
            "arguments": '"/k" python -m unittest discover -v',
            "description": "Run Application"
        }
    },

    "test": {
        "__init__.py": [],
        "test_<app_name>.py": [
            'import unittest\n',
            '\n',
            'class ApplicationTests(unittest.TestCase):\n',
            '\n',
            '    def setUp(self):\n',
            '        pass\n',
            '\n',
            '    def tearDown(self):\n',
            '        pass\n',
            '\n',
            '    def test_case_one(self):\n',
            '        self.assertTrue(True)\n',
            '\n'
            'if __name__ == "__main__":\n',
            '    unittest.main()\n',
        ]
    },

    "<app_name>": {
        "__init__.py": [],
        "<app_name>.py": [
            'import time\n',
            '\n',
            'def start_application():\n',
            '    print("test123")\n',
            '    time.sleep(5)\n'
            # 'def start_application():\n',
            # '    pass\n',
        ]
    }
}

PLACEHOLDER = "<app_name>"

class ProjectParameters():

    def __init__(self):
        self.app_name = None

        self.directories = {
            "start": None,
            "base": None,

            "others": {}
        }

    def prompt_for_project_parameters(self):

        app_name = self.app_name
        while app_name is None:
            app_name = input("What should be the name of the new app?: ")
            app_name = ProjectParameters.remove_whitespace(app_name)

        starting_directory = self.get_directory_or_default("start")
        while starting_directory is None:
            starting_directory = input("Enter the full path of the starting directory for the new project: ")
            #TODO: Add path validation

        self.app_name = app_name
        self.set_directory("start", starting_directory)

    def get_directory_or_default(self, directory: str):
        found_directory = self.directories.get(directory, "")
        if found_directory == "":
            return self.directories["others"].get(directory, "")
        return found_directory
    
    def set_directory(self, directory_name: str, directory: str):
        self.directories.update({directory_name: directory})

    def add_new_other_directory(self, directory_name):
        self.directories["others"].update(
            {directory_name: os.path.join(self.get_directory_or_default("base"), directory_name)})

    @classmethod
    def remove_whitespace(cls, value: str) -> str:
        value = value.split()
        return '_'.join(value)

    def validate_parameters(self, directory: str) -> bool:
        print("The new application will be created using the following parameters.\n")

        print(f"\tApp Name: {self.app_name}")
        print(f"\tStarting Directory: {self.get_directory_or_default(directory)}")

        return strtobool(input("Continue?"))

def start_application():
    project_params = ProjectParameters()
    project_params.prompt_for_project_parameters()
    if not project_params.validate_parameters("start"):
        wait_for_exit("Inputs not confirmed. Press any key to quit.")

    else:
        os.chdir(fr"{project_params.directories.get('start')}")

        project_params.set_directory(
            "base",
            os.path.join(
                project_params.get_directory_or_default("start"),
                project_params.app_name))

        os.mkdir(project_params.get_directory_or_default("base"))

        for directory in PROJECT_CONTENTS:
            if directory != "base":
                directory = replace_app_placeholder_in_string(directory, project_params.app_name)

                project_params.add_new_other_directory(directory)
                directory_in_progress = project_params.get_directory_or_default(directory)
            else:
                directory_in_progress = project_params.get_directory_or_default("base")

            if not os.path.exists(directory_in_progress):
                os.mkdir(directory_in_progress)

            os.chdir(directory_in_progress)
            create_directory_contents(directory, project_params)

        wait_for_exit("The app template has been created. Press any key to exit.")

def create_directory_contents(directory_name: str, project_params: ProjectParameters):
    full_directory_path = project_params.get_directory_or_default(directory_name)
    directory_name = replace_app_with_placeholder(directory_name, project_params.app_name)

    for _file, contents in PROJECT_CONTENTS.get(directory_name).items():
        _file = replace_app_placeholder_in_string(_file, project_params.app_name)
        contents = replace_app_placeholder_in_contents(contents, project_params.app_name)

        if _file[-4:len(_file)] == ".lnk":
            create_shortcut_in_directory(_file, full_directory_path, contents)
        else:
            create_file_in_directory(_file, full_directory_path, contents)

def replace_app_with_placeholder(name: str, app_name: str) -> str:
    return name.replace(app_name, PLACEHOLDER)

def replace_app_placeholder_in_string(name: str, app_name: str) -> str:
    return name.replace(PLACEHOLDER, app_name)

def replace_app_placeholder_in_contents(contents, app_name: str):
    if isinstance(contents, list):
        return [line.replace(PLACEHOLDER, app_name) for line in contents]

    elif isinstance(contents, dict):
        new_contents = dict()
        for key, value in contents.items():
            new_contents.update(
                {key.replace(PLACEHOLDER, app_name): value.replace(PLACEHOLDER, app_name)})
        return new_contents

    else:
        return contents

def create_shortcut_in_directory(file_name: str, directory: str, contents: list):
    link_full_path = os.path.join(directory, file_name)

    with winshell.shortcut(link_full_path) as shortcut:
        shortcut.path = contents.get("path")
        shortcut.description = contents.get("description")
        shortcut.arguments = contents.get("arguments")
        shortcut.working_directory = directory

def create_file_in_directory(file_name: str, directory: str, contents: list):
    open_file = open(os.path.join(directory, file_name), "w")

    if len(contents) > 0:
        open_file.writelines(contents)
        open_file.writable()

    open_file.close()

def wait_for_exit(prompt: str):
    input(prompt)

if __name__ == "__main__":
    start_application()
