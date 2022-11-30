from __future__ import annotations
import ruamel.yaml as yaml
from os.path import exists
from shutil import copyfile
from sys import exc_info
from ..models.config import Config
from ..helpers.logging import logger

# Relative path to config.yml and defaults.yml
config_path = 'assets/config.yml'
defaults_path = 'assets/defaults.yml'


def sort_model(models: list[Item] | list[Service] | list[Link]):
    return sorted(models, key=lambda x: (x.order, x.name))


def read_config() -> Config:
    logger.debug(f'Reading config at path {config_path}')

    with open(config_path, 'r') as file:
        try:
            config = Config(**yaml.safe_load(file))
        except yaml.YAMLError as exc:
            logger.error(f'Unable to read config file at path {config_path}. Error: {exc}')
    
    logger.debug('Config file read successfully')

    return config


def write_config(config: Config) -> Config:
    config.links = sort_model(config.links)
    config.services = sort_model(config.services)
    
    for service in config.services:
        service.items = sort_model(service.items)

    if config.defaults != None:
        if config.defaults.layout != None: 
            config.defaults.layout = config.defaults.layout.value

        if config.defaults.colorTheme != None:
            config.defaults.colorTheme = config.defaults.colorTheme.value

    config = config.dict()

    config = {k: v for (k, v) in config.items() if v != None}

    logger.debug(f'Writing new config to {config_path}')

    with open(config_path, 'w') as file:
        try:
            yaml.safe_dump(config, file)
        except yaml.YAMLError as exc:
            logger.error(f'Unable to write config. Error: {exc}')

    logger.debug(f'Config successfuly written')

    return read_config()


def verify_config_exists() -> Config:
    return exists(config_path)


def copy_defaults() -> None:
    if not exists(defaults_path):
        raise FileNotFoundError

    try:
        copyfile(defaults_path, config_path)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", exc_info())


def assign_missing_ids(models: list[Item] | list[Service] | list[Link]):
    logger.debug("Assigning Missing IDs...")
    if len(models) == 0:
        logger.debug("No Models Found")
        return models

    missing_ids = missing_order = list(filter(lambda x: x.id == None, models))

    if len(missing_ids) == 0:
        logger.debug("No models missing IDs")
        return models

    logger.debug("Assigning IDs")

    if len(missing_ids) == len(models):
        max_id = 1
    else:
        has_ids = list(filter(lambda x: x.id != None, models))
        max_id = max(has_ids, key=lambda x: x.id).id

    for elem in missing_ids:
        elem.id = max_id
        max_id += 1

    return models


def assign_missing_order(models: list[Item] | list[Service] | list[Link]):
    logger.debug("Assigning Missing Order...")
    if len(models) == 0:
        logger.debug("No Models Found")
        return models

    missing_order = list(filter(lambda x: x.order == None, models))

    if len(missing_order) != len(models):
        logger.debug("At least one model has an order")
        return models

    logger.debug("Assigning Order")

    order = 1
    for elem in models:
        elem.order = order
        order += 1

    return models


def add_id_and_order() -> Config:
    config = read_config()

    config.links = assign_missing_ids(config.links)
    config.services = assign_missing_ids(config.services)

    config.links = assign_missing_order(config.links)
    config.services = assign_missing_order(config.services)

    for service in config.services:
        service.items = assign_missing_ids(service.items)
        service.items = assign_missing_order(service.items)

    write_config(config)
