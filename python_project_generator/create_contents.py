from string import Template
import os
import json
import winshell
from python_project_generator.project_parameters import ProjectParameters

PROJECT_CONTENTS = {}

PLACEHOLDER = {
    "app": "${app_name}",
    "github": "${github_user}"
}

def load_project_contents():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    global PROJECT_CONTENTS

    open_file = open(os.path.join(current_directory, "project_contents.json"))
    PROJECT_CONTENTS = json.load(open_file)

    open_file.close()

    return PROJECT_CONTENTS

def create_directory_contents(directory_name: str, project_params: ProjectParameters):
    full_directory_path = project_params.get_directory_or_default(directory_name)

    for _file, contents in PROJECT_CONTENTS.get(directory_name).items():
        _file, contents = clean_data(_file, contents, project_params)

        create_file(_file, contents, full_directory_path)

def clean_data(_file: str, contents, project_params: ProjectParameters):
    _file = replace_placeholders_in_string(_file, project_params)
    contents = replace_app_placeholder_in_contents(contents, project_params)

    return _file, contents

def replace_placeholders_in_string(value: str, project_params: ProjectParameters) -> str:
    template = Template(value)
    return template.substitute(app_name=project_params.app_name, github_user=project_params.user)

def replace_app_placeholder_in_contents(contents, project_params: ProjectParameters):
    if isinstance(contents, list):
        return [
            Template(line).substitute(
                app_name=project_params.app_name,
                github_user=project_params.user) for line in contents]

    elif isinstance(contents, dict):
        new_contents = dict()
        for key, value in contents.items():
            new_contents.update(
                {Template(key).substitute(
                    app_name=project_params.app_name,
                    github_user=project_params.user):

                 Template(value).substitute(
                     app_name=project_params.app_name,
                     github_user=project_params.user)}
            )
        return new_contents

    else:
        return contents

def create_file(_file: str, contents, full_directory_path: str):
    if _file[-4:len(_file)] == ".lnk":
        create_shortcut_in_directory(_file, full_directory_path, contents)

    else:
        create_file_in_directory(_file, full_directory_path, contents)

def create_shortcut_in_directory(file_name: str, directory: str, contents: list):
    link_full_path = os.path.join(directory, file_name)

    with winshell.shortcut(link_full_path) as shortcut:
        shortcut.path = rf'{contents.get("path")}'
        shortcut.description = contents.get("description")
        shortcut.arguments = rf'{contents.get("arguments")}'
        shortcut.working_directory = directory

def create_file_in_directory(file_name: str, directory: str, contents: list):
    open_file = open(os.path.join(directory, file_name), "w")

    if len(contents) > 0:
        open_file.writelines(contents)
        open_file.writable()

    open_file.close()
