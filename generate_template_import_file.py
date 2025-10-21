import os
from datetime import datetime
import json

def version_from_date():
    """
    Turn the current date into a number representation to use a version
    EG: 10/25/2025 return 20251025
    :return:
    """
    current_date = datetime.now()
    return int(current_date.strftime("%Y%m%d"))


def get_all_macro_files():
    """
    Generates an array of dicts representing macros in the current working directory.
    [{
      name: 'name.macro',
      content: 'string of the macro content'
    }]
    :return: array of dicts containing a macro name and the file content
    """
    macros = []
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.endswith(".macro"):
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    current_macro = {"name": filename, "content": content}
                    macros.append(current_macro)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return macros

def read_and_marshall_atci_config():
    """
    Reads the ATCI.json config file to populate a shareable config file
    Returns an unmarshalled version of the json file to populate.
    :return: Dict of unmarshalled configuration file for ATCI
    """
    config_struct = None
    try:
        with open("ATCI.json", "r") as f:
            content = f.read()
            config_struct = json.loads(content)
            config_struct.pop('files', None)  # We do not really need the files key anymore after using it as validator
    except Exception as e:
        print(f"Problem reading atci.json: {e}")
    return config_struct

def generate_template_import_file():
    """
    Populates and writes a config file that can be imported into gSender.
    All macro files and the currently configured defaults within the ATCI.json file are populated into a new file
    Output file name is based on the current day.
    :return:
    """
    version = version_from_date()
    macros = get_all_macro_files()
    config = read_and_marshall_atci_config()

    config["version"] = version
    config["macros"] = macros

    try:
        filename = f"atci_templates_v{version}.json"
        with open(filename , "w") as f:
            json.dump(config, f)
            print(f"Output generated file: {filename}")
    except Exception as e:
        print(f"Unable to write out new template import: {e}")


if __name__ == "__main__":
    generate_template_import_file()