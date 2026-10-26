from dataclasses import dataclass
from typing import Dict, Optional, Tuple


MANDATORY_KEYS = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
OPTIONAL_KEYS = ["SEED"]
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
        A dict mapping each key to its raw value (both stripped).

    Raises:
        ConfigError: If the file can't be opened or a line is malformed.
    """
    pairs: Dict[str, str] = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise ConfigError(f"config file not found: {filepath}")
    except IsADirectoryError:
        raise ConfigError(f"{filepath} is a directory, not a file")
    except PermissionError:
        raise ConfigError(f"permission denied: {filepath}")
    except UnicodeDecodeError:
        raise ConfigError(f"{filepath} is not a valid text file")
    except OSError as e:
        raise ConfigError(f"can't read {filepath}: {e.strerror}")

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if line == "" or line.startswith('#'):
            continue
        if '=' not in line:
            raise ConfigError(f"line {line_num}: expected KEY=VALUE, "
                              f"got '{line}'")

        key, value = line.split('=', 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "":
            raise ConfigError(f"line {line_num}: missing key before '='")
        if value == "":
            raise ConfigError(f"line {line_num}: missing value for {key}")
        if key not in MANDATORY_KEYS and key not in OPTIONAL_KEYS:
            raise ConfigError(f"line {line_num}: unknown key '{key}'")
        if key in pairs:
            raise ConfigError(f"line {line_num}: {key} is defined twice")
        pairs[key] = value

    return pairs


def parse_int(key: str, value: str) -> int:
    """Convert a config value to int, with a readable error."""
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
    exit_ = parse_coords("EXIT", pairs["EXIT"])
    for key, (x, y) in (("ENTRY", entry), ("EXIT", exit_)):
        if not (0 <= x < width and 0 <= y < height):
            raise ConfigError(f"{key} {x},{y} is outside the maze "
                              f"({width}x{height})")
    if entry == exit_:
        raise ConfigError("ENTRY and EXIT must be different cells")

    seed = None
    if "SEED" in pairs:
        seed = parse_int("SEED", pairs["SEED"])

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=pairs["OUTPUT_FILE"],
        perfect=parse_bool("PERFECT", pairs["PERFECT"]),
        seed=seed,
    )
