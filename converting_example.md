AHK SCRIPT:
```ahk
::ae:ä
::ue:ü
```
---
PYTHON SCRIPT:
*After some magic with convert*

```python
import keyboard as kb
import re

def convert_hotkey(line: str) -> str:
  # ^j::Send, Hello -> kb.add_hotkey("ctrl+j", lambda: kb.write("Hello"))
```

Not so hard, yeah?
**We'll see how many years I'll spend on it xD**
