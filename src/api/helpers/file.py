import ruamel.yaml as yaml
from os.path import exists
from shutil import copyfile
from sys import exc_info

# Relative path to config.yml and defaults.yml
config_path = 'assets/config.yml'
defaults_path = 'assets/defaults.yml'


def read_config():
    with open(config_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)


def write_config(config):
    with open(config_path, 'w') as file:
        try:
            yaml.safe_dump(config, file)
        except yaml.YAMLError as exc:
            print(exc)

    return read_config()


def verify_config_exists():
    return exists(config_path)


def copy_defaults():
    if not exists(defaults_path):
        raise FileNotFoundError

    try:
        copyfile(defaults_path, config_path)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", exc_info())
