from dataclasses import dataclass
from enum import Enum
import re  # For modifier parsing
from pathlib import Path  # For read .ahk files


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
    """
    Parse hotkey/hotstring: trigger (including modifiers), replacement.
    """
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


def main(file: str = "test.ahk") -> None:
    content = Path(file).read_text(encoding="utf-8")
    # New method of reading file, recently saw
    # Works good
    for line in content.splitlines():  # splitting lines to...
        # avoid issues with spaces
        # Parsing a file to take all lines
        trigger, replacement = parse_hotkeys(line)
        if trigger is not None and replacement is not None:
            print(f" Trigger: {trigger} -> Replacement: {replacement}")


if __name__ == "__main__":
    main("test_script.ahk")
