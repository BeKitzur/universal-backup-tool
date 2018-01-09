#!/usr/bin/env python3

"""
Usage:
    unibackup [options]

    -h --help  Show help
    -c <config> --config=<config>  Configuration file
"""
from docopt import docopt
import yaml
import backup


def load_yaml_config(config_file):
    with open(config_file, 'r') as yaml_file:
        config = yaml.load(yaml_file)

    return config


def merge(dict_1, dict_2):
    """Merge two dictionaries.
    Values that evaluate to true take priority over false values.
    `dict_1` takes priority over `dict_2`.
    """
    return dict((str(key), dict_1.get(key) or dict_2.get(key))
                for key in set(dict_2) | set(dict_1))


def main():
    arguments = docopt(__doc__, version='0.1')
    config_file = arguments['--config']

    # NOTE: Maybe we don't even need this
    if config_file is not None:
        yaml_config = load_yaml_config(config_file)
        backup.config = merge(arguments, yaml_config)
    else:
        backup.config = arguments

    backup.run()


if __name__ == '__main__':
    main()
