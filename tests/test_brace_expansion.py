from brace_expansion import expand_braces


def test_simple_expansion():
    assert expand_braces("echo a{b,c}d") == "echo abd acd"


def test_multiline_command_preserved():
    # Regression test for issue #4 / PR #5: a multiline command (e.g. a
    # Python for-loop) must keep its newlines and indentation, otherwise
    # xonsh fails to parse it.
    cmd = "for i, x in enumerate('xonsh'):\n    print(i, x)"
    assert expand_braces(cmd) == cmd


def test_whitespace_inside_quotes_preserved():
    # "a  b" must not be split then joined with a single space.
    cmd = 'echo "a  b" {x,y}'
    assert expand_braces(cmd) == 'echo "a  b" x y'


def test_env_var_lookup_not_expanded():
    # ${VAR} is an environment-variable lookup in xonsh, not a brace
    # expansion: it must be left alone.
    cmd = "echo ${HOME}"
    assert expand_braces(cmd) == cmd


def test_python_set_literal_not_expanded():
    cmd = "print({1,2,3})"
    assert expand_braces(cmd) == cmd


def test_python_dict_literal_not_expanded():
    cmd = "d = {'a':1,'b':2}"
    assert expand_braces(cmd) == cmd


def test_subproc_inside_python_block_expanded():
    cmd = "for i in range(3):\n    echo a{b,c}"
    assert expand_braces(cmd) == "for i in range(3):\n    echo ab ac"


def test_python_literal_inside_python_block_not_expanded():
    cmd = "for i in range(3):\n    print({i,i+1})"
    assert expand_braces(cmd) == cmd
