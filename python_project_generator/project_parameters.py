import os
from distutils.util import strtobool

class ProjectParameters():

    directory_default = ""

    def __init__(self):
        self.app_name = None
        self.user = None

        self.directories = {
            "start": ProjectParameters.directory_default,
            "base": ProjectParameters.directory_default,

            "others": {}
        }

    def prompt_for_project_parameters(self):

        app_name = self.app_name
        while app_name is None:
            app_name = input("What should be the name of the new app?: ")
            app_name = ProjectParameters.remove_whitespace(app_name)

        starting_directory = self.get_directory_or_default("start")
        while starting_directory is ProjectParameters.directory_default:
            starting_directory = input("Enter the full path of the starting directory for the new project: ")
            #TODO: Add path validation

        user = self.user
        while user is None:
            user = input("Enter your github usernam (used for LICENSE): ")

        self.app_name = app_name
        self.user = user
        self.set_named_directory("start", starting_directory)

    def get_directory_or_default(self, directory: str):
        found_directory = self.directories.get(directory, ProjectParameters.directory_default)
        if found_directory == "":
            return self.directories["others"].get(directory, ProjectParameters.directory_default)
        return found_directory

    def set_named_directory(self, directory_name: str, directory: str):
        self.directories.update({directory_name: directory})

    def add_new_other_directory(self, directory_name):
        self.directories["others"].update(
            {directory_name: os.path.join(self.get_directory_or_default("base"), directory_name)})

    @classmethod
    def remove_whitespace(cls, value: str) -> str:
        value = value.split()
        return '_'.join(value)

    def validate_parameters(self, directory: str) -> bool:
        print("\nThe new application will be created using the following parameters.\n")

        print(f"\tApp Name: {self.app_name}")
        print(f"\tStarting Directory: {self.get_directory_or_default(directory)}")
        print(f"\tGithub User: {self.user}")

        try:
            return strtobool(input("Continue?"))
        except ValueError:
            return False
