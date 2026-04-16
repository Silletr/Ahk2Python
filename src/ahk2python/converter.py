from pathlib import Path

from keyboard import add_hotkey, wait, write

from parser import parse_hotkeys


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃                              Cloned from parser.main                               ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def open_and_analyse(file: str = "test.ahk"):
    content = Path(file).read_text(encoding="utf-8")
    for line in content.splitlines():
        #    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        #    ┃                                 splitting lines to                                 ┃
        #    ┃                              avoid issues with spaces                              ┃
        #    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        #  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Parsing a file to take all lines ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        results = []

        for line in content.splitlines():
            trigger, replacement = parse_hotkeys(line)
            if trigger is not None and replacement is not None:
                results.append((trigger, replacement))
            else:
                print("Trigger and Replacement is None")
                results.append("Trigger empty, Replacement also none")
        return results


def convert(file: str = "main.ahk") -> list[tuple[str, str]]:
    """
    Creates hotkey using keyboard.add_hotkey().
    Args:
        file: str, default flie to analyse: "main.ahk" - Takes an FILE name;
        and creating hotkey's for every bind corresponding Trigger
    """
    content = Path(file).read_text(encoding="utf-8")
    bindings: list[tuple[str, str]] = []
    #  ───────────────────────────────── Trigger -> Replacement ─────────────────────────────────
    AHK_TO_KEYBOARD = {
        "#": "win",
        "^": "ctrl",
        ">^": "LCtrl",
        "<!": "LAlt",
        ">!": "RAlt",
        "<+": "LShift",
        ">+": "RShift",
    }

    for line in content.splitlines():
        trigger, replacement = parse_hotkeys(line)
        if trigger is None or replacement is None:
            continue

        print(f"Trigger: {trigger} -> Replacement: {replacement}")

        key = trigger.strip()
        modifiers = []
        for sym, kb_mod in AHK_TO_KEYBOARD.items():
            if sym in key:
                modifiers.append(kb_mod)
                key = key.replace(sym, "")

        if not key:
            print("Warning: no key after modifiers")
            continue

        hotkey = "+".join(modifiers) + ("+" + key if modifiers else key)
        print(f"Hotkey for keyboard: {hotkey!r}")

        add_hotkey(
            hotkey, lambda rep=replacement: write(rep.replace("Send, ", "").strip())
        )
        bindings.append((trigger, replacement))

    return bindings


#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    Keep the script alive (keyboard listeners stay active)    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
bindings = convert("./test_script.ahk")
print(bindings)
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#    ┃    Press "esc" to quiet    ┃
#    ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

wait()
