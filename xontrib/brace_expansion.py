"""
Implements Bash-style brace expansion:

```console
@ echo a{d,c,b}e
ade ace abe
@ echo /usr/{ucb/{ex,edit},lib/{ex?.?*,how_ex}}
/usr/ucb/ex /usr/ucb/edit /usr/lib/ex?.?* /usr/lib/how_ex
```

See also:
* https://facelessuser.github.io/bracex/
* https://www.gnu.org/software/bash/manual/html_node/Brace-Expansion.html
"""
import bracex
from xonsh.events import events


def _expand_line(line: str) -> str:
    if "{" not in line:
        return line

    # Preserve leading whitespace
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]

    expanded_parts = [
        expansion
        for part in stripped.split()
        for expansion in bracex.expand(part)
    ]
    return indent + " ".join(expanded_parts)


@events.on_transform_command
def expand_braces(cmd, **_):
    return "\n".join(_expand_line(line) for line in cmd.split("\n"))
