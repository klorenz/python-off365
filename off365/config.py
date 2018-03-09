from os import chmod, makedirs
from os.path import exists, dirname, expanduser
import pyaml
import yaml
from .msgraph_api import MSGraphApi


def read_config_file():
    config_file = expanduser("~/.config/off365/config")
    try:
        with open(config_file, 'r') as f:
            result = yaml.load(f)
        if result is None:
            result = {}
        return result

    except:
        write_config_file({})
        return {}


def write_config_file(data):
    config_file = expanduser("~/.config/off365/config")
    if not exists(dirname(config_file)):
        makedirs(dirname(config_file))

    with open(config_file, 'w') as f:
        f.write(pyaml.dump(data))

    chmod(config_file, 0600)


def get_config(name):
    try:
        return read_config_file()[name]
    except:
        raise Exception("You have to create a config with `off365 config`")


def get_api(config):
    return MSGraphApi(**get_config(config))
