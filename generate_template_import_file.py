import os
from datetime import datetime
import json

def version_from_date():
    current_date = datetime.now()
    return int(current_date.strftime("%Y%m%d"))


def get_all_macro_files():
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
    config_struct = None
    try:
        with open("ATCI.json", "r") as f:
            content = f.read()
            config_struct = json.loads(content)
    except Exception as e:
        print(f"Problem reading atci.json: {e}")
    return config_struct

def generate_template_import_file():
    version = version_from_date()
    macros = get_all_macro_files()
    config = read_and_marshall_atci_config()
    config.pop('files', None) # We do not really need the files key anymore after using it as validator

    config["version"] = version
    config["macros"] = macros

    try:
        with open(f"atci_templates_v{version}.json" , "w") as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Unable to write out new template import: {e}")


    print(config)


if __name__ == "__main__":
    generate_template_import_file()