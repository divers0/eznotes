import json
import os

from ..const import CONFIG_FILE_PATH
from ..exceptions import ConfigFileDoesNotExist


def config_file_initiate():
    from .editor import editor_initiate
    write_to_config_file({})
    editor_initiate()
    change_value_in_conf("trash", True)


def config_file_exists():
    if os.path.isfile(CONFIG_FILE_PATH):
        return True
    return False


def config_file_valid():
    if all((config_file_has_key("editor"), config_file_has_key("trash"))):
        return True
    return False


def get_config_file():
    if not config_file_exists():
        raise ConfigFileDoesNotExist

    with open(CONFIG_FILE_PATH) as f:
        conf_file = json.load(f)

    return conf_file


def write_to_config_file(new_config):
    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(new_config, f)


def get_value_from_config_file(key):
    if config_file_has_key(key):
        return get_config_file()[key]


def change_value_in_conf(key, value):
    conf_file = get_config_file()
    conf_file[key] = value
    write_to_config_file(conf_file)


def config_file_has_key(key):
    if not config_file_exists():
        return False

    conf_file = get_config_file()

    if key in conf_file:
        return True
    return False
