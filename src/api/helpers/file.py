from __future__ import annotations
import ruamel.yaml as yaml
from os.path import exists
from os import remove
from shutil import copyfile
from sys import exc_info
from ..models.config import Config
from ..helpers.logging import logger
from fastapi import HTTPException
from re import search
from .exceptions import InvalidConfigPathError, EmptyFileError, NoChangesMade

# Relative path to config.yml and defaults.yml
config_path = 'assets/config.yml'
defaults_path = 'assets/defaults.yml'

def verify_config_path(path: str | None, verify_exists: bool = True) -> Config:
    if path == None:
        path = config_path

    if not search(r"^([A-z0-9-_+]+\/)*([A-z0-9]+\.(yml))$", path):
        raise InvalidConfigPathError

    if not exists(path) and verify_exists:
        raise FileNotFoundError

    return path

def read_config(path: str | None) -> Config:
    path = verify_config_path(path)

    logger.debug(f'Reading config at path {path}')

    with open(path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            logger.error(f'Unable to read config file at path {path}. Error: {exc}')
    
    if config == '' or not config:
        raise EmptyFileError

    config['colors'] = { k1 : { k2.replace('-', '_') : v2 for k2,v2 in v1.items()} for k1, v1 in config['colors'].items() }

    logger.debug('Config file read successfully')

    return Config(**config)

def read_config_http(path: str | None) -> Config:
    try:
        return read_config(path)
    except FileNotFoundError:
        raise HTTPException(409, f'Config file not found at path {path}')
    except InvalidConfigPathError:
        raise HTTPException(400, 'CONFIG-PATH must point to a .yml file')
    except EmptyFileError:
        raise HTTPException(410, 'Config file empty')

def write_config(path: str | None, config: Config) -> Config:
    path = verify_config_path(path, verify_exists=False)

    old_config = read_config(path).dict()
    
    if config.defaults:
        if config.defaults.layout: 
            config.defaults.layout = config.defaults.layout.value

        if config.defaults.colorTheme:
            config.defaults.colorTheme = config.defaults.colorTheme.value

    config.clean()

    config = config.dict()

    config = {k: v for (k, v) in config.items() if v != None}

    config['links'] = [{k: v for (k, v) in x.items() if v != None} for x in config['links']]
    config['services'] = [{k: v for (k, v) in x.items() if v != None} for x in config['services']]
    
    for service in config['services']:
        service['items'] = [{k: v for (k, v) in x.items() if v != None} for x in service['items']]

    config['colors'] = { k1 : { k2.replace('_', '-') : v2 for k2,v2 in v1.items()} for k1, v1 in config['colors'].items() }

    logger.debug(f'Writing new config to {path}')

    with open(path, 'w') as file:
        try:
            yaml.safe_dump(config, file)
            logger.debug(f'Config successfuly written')
        except yaml.YAMLError as exc:
            logger.error(f'Unable to write config. Error: {exc}')
            yaml.safe_dump(old_config, file)
            logger.info('Reverted to previous file')
            raise NoChangesMade

    return read_config(config_path)

def write_config_http(path: str | None, config: Config):
    try:
        return write_config(path, config)
    except InvalidConfigPathError:
        raise HTTPException(400, 'CONFIG-PATH must point to a .yml file')
    except NoChangesMade:
        raise HTTPException(409, 'Unable to write config. Reverted to previous file')

def copy_defaults(path: str | None) -> None:
    path = verify_config_path(path, verify_exists=False)
    
    try:
        copyfile(defaults_path, path)
    except IOError as e:
        print("Unable to copy file. %s" % e)
    except:
        print("Unexpected error:", exc_info())

    write_config_http(path, read_config_http(None))

def delete_file(path: str) -> None:
    path = verify_config_path(path)
    
    remove(path)