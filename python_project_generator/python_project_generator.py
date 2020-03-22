import os
from python_project_generator.project_parameters import ProjectParameters
from python_project_generator.create_contents import (create_directory_contents, replace_placeholders_in_string,
                                                      load_project_contents, replace_placeholders_in_string, PROJECT_CONTENTS)

def start_application():
    project_params = get_valid_parameters()

    if project_params is not None:
        global PROJECT_CONTENTS
        PROJECT_CONTENTS = load_project_contents()

        os.chdir(fr"{project_params.directories.get('start')}")

        prepare_base_directory(project_params)
        create_project_content(project_params)

        print("\nNote: The default license is MIT. If this is not appropriate for you project," \
              " you should replace it.")

        wait_for_exit("\nThe app template has been created. Press any key to exit.")

def get_valid_parameters():
    parameters = ProjectParameters()
    parameters.prompt_for_project_parameters()

    if not parameters.validate_parameters("start"):
        parameters = None
        wait_for_exit("Inputs not confirmed. Press any key to quit.")

    return parameters

def prepare_base_directory(project_params: ProjectParameters):
    project_params.set_named_directory(
        "base",
        os.path.join(
            project_params.get_directory_or_default("start"),
            project_params.app_name))

    os.mkdir(project_params.get_directory_or_default("base"))

def create_project_content(project_params: ProjectParameters):
    for directory in PROJECT_CONTENTS:
        print(f"Creating {replace_placeholders_in_string(directory, project_params)} directory")

        if directory != "base":
            directory_in_progress = create_inner_directory(directory, project_params)

        else:
            directory_in_progress = create_base_directory(project_params)

        move_to_directory(directory_in_progress)
        create_directory_contents(directory, project_params)

def create_inner_directory(directory: str, project_params: ProjectParameters):
    directory = replace_placeholders_in_string(directory, project_params)

    project_params.add_new_other_directory(directory)
    return project_params.get_directory_or_default(directory)

def create_base_directory(project_params: ProjectParameters):
    return project_params.get_directory_or_default("base")

def move_to_directory(directory: str):
    if not os.path.exists(directory):
        os.mkdir(directory)

    os.chdir(directory)

def wait_for_exit(prompt: str):
    input(prompt)

if __name__ == "__main__":
    start_application()
