from dataclasses import dataclass
from typing import Dict, Optional, Tuple


MANDATORY_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
MAX_SIZE = 200


class ConfigError(Exception):
    """Raised when the config file can't be read or has invalid values."""


@dataclass
class MazeConfig:
    """Validated settings read from the config file."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def read_pairs(filepath: str) -> Dict[str, str]:
    """Read KEY=VALUE pairs from a file.

    Empty lines and lines starting with '#' are skipped.

    Args:
        filepath: Path of the config file.

    Returns:
        A dict mapping each key to its value.

    Raises:
        ConfigError: If the file can't be read or a line is malformed.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except OSError as e:
        raise ConfigError(f"can't read {filepath}: {e.strerror}")
    except UnicodeDecodeError:
        raise ConfigError(f"{filepath} is not a text file")

    pairs: Dict[str, str] = {}
    line_num = 0
    for line in lines:
        line_num += 1
        line = line.strip()
        if line == "" or line.startswith('#'):
            continue
        if '=' not in line:
            raise ConfigError(f"line {line_num}: expected KEY=VALUE, "
                              f"got '{line}'")

        key, value = line.split('=', 1)
        key = key.strip().upper()
        value = value.strip()
        if key == "" or value == "":
            raise ConfigError(f"line {line_num}: empty key or value")
        pairs[key] = value

    return pairs


def parse_int(key: str, value: str) -> int:
    """Convert a config value to int."""
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} must be an integer, got '{value}'")


def parse_coords(key: str, value: str) -> Tuple[int, int]:
    """Convert an 'x,y' config value to a tuple of two ints."""
    parts = value.split(',')
    if len(parts) != 2:
        raise ConfigError(f"{key} must look like x,y, got '{value}'")
    x = parse_int(key, parts[0].strip())
    y = parse_int(key, parts[1].strip())
    return (x, y)


def parse_bool(key: str, value: str) -> bool:
    """Convert 'True' or 'False' (any case) to a bool."""
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise ConfigError(f"{key} must be True or False, got '{value}'")


def parse_config(filepath: str) -> MazeConfig:
    """Read and validate the maze config file.

    Args:
        filepath: Path of the config file.

    Returns:
        A MazeConfig with every value converted and checked.

    Raises:
        ConfigError: If the file is missing, malformed or has bad values.
    """
    pairs = read_pairs(filepath)

    for key in MANDATORY_KEYS:
        if key not in pairs:
            raise ConfigError(f"missing mandatory key: {key}")

    width = parse_int("WIDTH", pairs["WIDTH"])
    height = parse_int("HEIGHT", pairs["HEIGHT"])
    if width < 1 or height < 1:
        raise ConfigError("WIDTH and HEIGHT must be at least 1")
    if width > MAX_SIZE or height > MAX_SIZE:
        raise ConfigError(f"WIDTH and HEIGHT can't be more than {MAX_SIZE}")

    entry = parse_coords("ENTRY", pairs["ENTRY"])
    exit_pos = parse_coords("EXIT", pairs["EXIT"])
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError(f"ENTRY {pairs['ENTRY']} is outside the maze")
    if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
        raise ConfigError(f"EXIT {pairs['EXIT']} is outside the maze")
    if entry == exit_pos:
        raise ConfigError("ENTRY and EXIT must be different cells")

    seed = None
    if "SEED" in pairs:
        seed = parse_int("SEED", pairs["SEED"])

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_pos,
        output_file=pairs["OUTPUT_FILE"],
        perfect=parse_bool("PERFECT", pairs["PERFECT"]),
        seed=seed,
    )
