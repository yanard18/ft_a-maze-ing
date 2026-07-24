import sys
from typing import Dict


def parse_config(filepath: str) -> Dict[str, str]:
    config = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 2)
                config[key] = value
    return config


def test_parser() -> None:
    config_file = sys.argv[1]
    maze_config = parse_config(config_file)
    for key, value in maze_config.items():
        print(f"{key}: {value}", end="")


test_parser()
