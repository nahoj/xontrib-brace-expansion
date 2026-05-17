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
from xonsh.parsers.lexer import Lexer

_lexer = Lexer(tolerant=True)


def _is_valid_python(src: str) -> bool:
    try:
        compile(src, "<brace_expansion>", "exec")
    except SyntaxError:
        return False
    return True


def _expand_line(line: str) -> str:
    if "{" not in line:
        return line

    # Preserve leading whitespace
    stripped = line.lstrip()
    indent = line[: len(line) - len(stripped)]

    # Don't expand a valid Python line (in which {} means dict/set).
    # This does not catch lines that are part of multiline statements
    # such as `if True:` or `"a": 1,`.
    if _is_valid_python(stripped):
        return line

    try:
        tokens = _lexer.split(stripped)
    except Exception:
        return line
    if not tokens:
        return line

    expanded_parts = [
        expansion
        for token in tokens
        for expansion in bracex.expand(token)
    ]
    return indent + " ".join(expanded_parts)


@events.on_transform_command
def expand_braces(cmd, **_):
    return "\n".join(_expand_line(line) for line in cmd.split("\n"))
