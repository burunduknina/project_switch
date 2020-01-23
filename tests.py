import pytest

from switch.switch_support import exec
from switch.switch_support import support_switch


def test_exec_general():
    """
    Check general functionality of exec function.
    """
    a, b, c = 2, 4, 5

    d = None
    loc = locals()
    exec(
        """switch a*a:
        case b:
            d = 1
            break
        case c:
            d = 2
            break
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 1


def test_support_switch_general():
    """
    Check general functionality of support_switch decorator.
    """

    @support_switch
    def my_function_with_switch(a: int, b: int, c: int):
        """
        switch a:
             case b:
                  return True
             case c:
                  return False
        """

    assert my_function_with_switch(2 * 2, 4, 5)


def test_default_handling():
    """
    Check handling of switch-case-default statement.
    """
    a, b, c = 2, 3, 5

    d = None
    loc = locals()
    exec(
        """switch a*a:
        case b:
            d = 1
            break
        case c:
            d = 2
            break
        default:
            d = 3
            break
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 3


def test_nesting():
    """
    Check handling of nested switch-case statement.
    """
    a, b, c, n = 2, 3, 4, True

    d = 0
    loc = locals()
    exec(
        """switch a*a:
        case b:
            d += 10
            break
        case c:
            d += 20
            switch n:
                case False:
                    d += 1
                    break
                case True:
                    d += 2
                    break
            break
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 22


def test_blank_lines():
    """
    Check handling of blank lines and wrap lines.
    """
    a, b, c = 2, 4, 5

    d = None
    loc = locals()
    exec(
        """switch [
            ] or a*a:
            
        case b:
        
            d = 1

            break
                
        case c:
            d = 2
            break
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 1


def test_handling_code_with_trailing_whitespace():
    """
    Check that code with trailing whitespaces handling correctly.
    """
    a, b, c = 2, 4, 5

    d = None
    loc = locals()
    exec(
        """switch a*a: 
        case b: 
            d = 1 
            break
        case c:
            d = 2
            break
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 1


def test_break_missing():
    """
    Check that 'break' missing handling correctly.
    """
    a, b, c = 2, 4, 5

    d = None
    loc = locals()
    with pytest.raises(SyntaxError) as exc:
        exec(
            """switch a*a:
            case b:
                d = 1
            case c:
                d = 2
                break
        """,
            globals(),
            loc,
        )
    assert 'Control cannot fall through from one case label to another.' \
           in str(exc.value)


def test_case_missing():
    """
    Check that 'case' missing handling correctly.
    """
    a, b, c = 2, 4, 5

    d = None
    loc = locals()
    with pytest.raises(SyntaxError) as exc:
        exec(
            """switch a*a:
            cas b:
                d = 1
                break
            cas c:
                d = 2
                break
        """,
            globals(),
            loc,
        )
    assert 'Incorrect syntax of switch-case statement.' \
           in str(exc.value)


def test_python_code_combination():
    """
    Check that switch-case statement can be combined with python code.
    """
    a, b, c = 2, 4, 5

    d = 0
    loc = locals()
    exec(
        """d += 100\nswitch a*a:
        case b:
            d += 10
            break
        case c:
            d += 20
            break\nd +=1
    """,
        globals(),
        loc,
    )
    assert loc["d"] == 111


def test_python_code_handling():
    """
    Check that code wo switch-case statement handling correctly.
    """
    a, b, c = 2, 4, 5

    d = 0
    loc = locals()
    exec(
        """d += 100\nd +=1""",
        globals(),
        loc,
    )
    assert loc["d"] == 101
