from dataclasses import dataclass
from enum import Enum
import re  # For modifier parsing


class LineType(Enum):
    HOTSTRING = "hotstring"  # ::ae::ä
    HOTKEY = "hotkey"  # ^j::Send, text
    COMMENT = "comment"
    EMPTY = "empty"
    UNKNOWN = "unknown"


@dataclass
class AHKLine:
    raw: str
    line_type: LineType
    data: dict


def parse_hotkeys(line: str) -> tuple[str | None, str | None]:
    """Parse hotkey/hotstring: trigger (incl. modifiers), replacement."""
    line = line.strip()
    if not line or line.startswith(";"):
        return None, None

    # Match hotkey/hotstring: optional modifiers + key :: replacement
    match = re.match(r"^(.+?::)(.+)$", line)
    if not match:
        return None, None

    trigger = match.group(1).rstrip("::")  # e.g., "^j" or "ae"
    replacement = match.group(2).lstrip()  # e.g., "Send, Hello World"
    return trigger, replacement


def classify_line(line: str) -> AHKLine:
    stripped = line.strip()
    if not stripped:
        return AHKLine(raw=line, line_type=LineType.EMPTY, data={})
    if stripped.startswith(";"):
        return AHKLine(raw=line, line_type=LineType.COMMENT, data={})

    # Check for :: pattern (both hotkeys/hotstrings)
    if "::" in stripped:
        # Quick type check: hotkeys have modifiers before first ::
        if re.match(r"^[^:]+::", stripped):
            return AHKLine(raw=line, line_type=LineType.HOTKEY, data={})
        elif stripped.startswith("::"):
            return AHKLine(raw=line, line_type=LineType.HOTSTRING, data={})

    return AHKLine(raw=line, line_type=LineType.UNKNOWN, data={})


# Fixed main loop
with open("test_script.ahk", "r") as file:
    for line in file:
        parsed = parse_hotkeys(line)
        if parsed[0] is not None:
            print(parsed)  # Only print valid hotkeys/hotstrings
