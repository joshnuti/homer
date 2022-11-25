import ruamel.yaml as yaml

# Relative path to config.yaml
config_path = 'assets/config.yml'

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