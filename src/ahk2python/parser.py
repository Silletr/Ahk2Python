from dataclasses import dataclass
from enum import Enum


class LineType(Enum):
    HOTSTRING = "hotstring"  # ::ae:ä
    HOTKEY = "hotkey"  # ^j::Send, text
    COMMENT = "comment"  # ; <- comment
    EMPTY = "empty"
    UNKNOWN = "unknown"


@dataclass
class AHKLine:
    raw: str
    line_type: LineType
    data: dict  # Aready parsed values


def parse_hotkeys(line: str) -> tuple[str, str]:
    """Parse hotstring into trigger and replacement."""
    rest = line[2:]  # remove opening ::
    parts = rest.split(":", 1)  # split on FIRST colon only
    trigger = parts[0]
    replacement = parts[1].lstrip(":")  # remove extra : if ::
    return trigger, replacement


def classify_line(line: str) -> AHKLine:
    line = line.strip()

    if not line:
        return AHKLine(raw=line, line_type=LineType.EMPTY, data={})
    if line.startswith(";"):
        return AHKLine(raw=line, line_type=LineType.COMMENT, data={})

    if line.startswith("::") and ":" in line[2:]:
        return AHKLine(raw=line, line_type=LineType.HOTSTRING, data={})

    return AHKLine(raw=line, line_type=LineType.UNKNOWN, data={})


print(parse_hotkeys("::ae:ä"))
print(parse_hotkeys("::ae::ä"))
