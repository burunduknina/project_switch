import inspect
import random
import re

old_exec = exec
SWITCH = 6


def exec(code, _globals=None, _locals=None):
    """
    Overrode built-in function with support switch-case statement.
    :param code: String with the code to execute.
    :param _globals: A dictionary of available global methods and variables.
    :param _locals: A dictionary of available local methods and variables.
    """
    python_code = change_code(code)
    old_exec(python_code, _globals, _locals)


def support_switch(func):
    """
    Decorator to execute docstring of a functions instead of code.
    Support switch-case statement.
    """

    def wrapper(*args, **kwargs):
        arguments = ""
        for i in args:
            arguments = f"{arguments}{str(i)}, "
        for key, value in kwargs.items():
            arguments = f"{arguments}{str(key)} = {str(value)}, "
        func_name = func.__name__
        python_code = change_code(func.__doc__)
        func_definition = f"def {func_name} {inspect.signature(func)}:\n"
        func_return = f"\n{func_name}_result = {func_name} ({arguments})"
        python_code = "".join((func_definition, python_code, func_return))
        result = {}
        old_exec(python_code, {}, result)
        return result[f"{func_name}_result"]

    wrapper.__name__ = f"func_{func.__name__}"

    return wrapper


def change_code(code):
    """
    Function to replace switch-case statements to if-else.
    :param code: String with the code to handle.
    :return: String with updated code.
    """
    draft_code_lines = code.rstrip().split("\n")
    code_lines = [
        line
        for line in draft_code_lines
        if re.search(r"[^ \t]", line) is not None
    ]
    for i, _ in enumerate(code_lines):
        code_lines[i] = code_lines[i].rstrip()
    code_length = len(code_lines)
    line_id = 0
    while line_id < code_length:
        line = code_lines[line_id]
        switch_marker = re.match(r"[ \t]*switch", line)
        if switch_marker:
            line_id = handle_switch_block(
                code_length, code_lines, line, line_id, switch_marker
            )
        else:
            line_id += 1
    return "\n".join(code_lines)


def handle_switch_block(code_length, code_lines, line, line_id, switch_marker):
    """
    Function to replace switch-case statement.
    :param code_length: Number of lines in code.
    :param code_lines: list of code lines.
    :param line: First line of switch-case statement.
    :param line_id: Index of first line of switch-case statement.
    :param switch_marker: Match Objects.
    :return: Index of last line of switch-case statement.
    """
    switch_begin = line[: switch_marker.end() - SWITCH]
    begin_len = len(switch_begin)
    end_switch_id = line_id + 1
    while end_switch_id < code_length and (
        re.match(r"[ \t]*", code_lines[end_switch_id]).end() > begin_len
    ):
        end_switch_id += 1
    change_switch_to_if(line_id, end_switch_id - 1, code_lines, switch_begin)
    return end_switch_id


def change_switch_to_if(begin_switch_id, end_switch_id, code_lines, begin):
    """
    Function to parse and handle switch-case statement.
    :param begin_switch_id: Index of first line of switch-case statement.
    :param end_switch_id: Index of last line of switch-case statement.
    :param code_lines: list of code lines.
    :param begin: Indent for switch.
    """
    var = "__switch_expression" + str(random.randint(100000, 1000000))
    break_flag = 0
    code_lines[begin_switch_id] = re.sub(
        "switch", f"{var} =", code_lines[begin_switch_id]
    )
    line_id = def_switch(code_lines, begin_switch_id + 1, end_switch_id)
    case_begin = re.match(r"[\ \t]*", code_lines[line_id + 1]).group(0)
    code_lines[line_id] = re.sub(
        r"[ \t]*case ", f"{begin}if {var} == ", code_lines[line_id]
    )
    while line_id < end_switch_id:
        line_id += 1
        line = code_lines[line_id]
        case_mark = re.match(r"[ \t]*case", line)
        if case_mark:
            break_flag = check_break_flag(break_flag)
            code_lines[line_id] = re.sub(
                r"[ \t]*case", f"{begin}elif {var} == ", line
            )
        else:
            break_mark = re.match(f"{case_begin}break", line)
            if break_mark:
                if (
                    line_id < end_switch_id
                    and (re.match(case_begin, code_lines[line_id + 1]) is None)
                    or line_id == end_switch_id
                ):
                    code_lines[line_id] = re.sub(
                        "break", "pass", code_lines[line_id]
                    )
                    break_flag = 1
            else:
                return_mark = re.match(f"{case_begin}return", line)
                if return_mark:
                    break_flag = 1
                else:
                    default_mark = re.match(r"[ \t]*default", line)
                    if default_mark:
                        break_flag = check_break_flag(break_flag)
                        code_lines[line_id] = re.sub(
                            r"[ \t]*default", f"{begin}else", line
                        )
                    else:
                        switch_mark = re.match(r"[ \t]*switch", line)
                        if switch_mark:
                            line_id = (
                                handle_switch_block(
                                    end_switch_id + 1,
                                    code_lines,
                                    line,
                                    line_id,
                                    switch_mark,
                                )
                                - 1
                            )
    check_break_flag(break_flag)


def def_switch(code_lines, line_id, end_switch_id):
    """
    Function to find the end of the switch definition.
    :param code_lines: list of code lines.
    :param line_id: Index of first line of switch-case statement.
    :param end_switch_id: Index of last line of switch-case statement.
    :return: Index of first line of case block.
    """
    case_mark = re.match(r"[ \t]*case", code_lines[line_id])
    while line_id < end_switch_id and not case_mark:
        line_id += 1
        case_mark = re.match(r"[ \t]*case", code_lines[line_id])
    if case_mark and code_lines[line_id - 1][-1] == ":":
        code_lines[line_id - 1] = code_lines[line_id - 1][:-1]
    else:
        raise SyntaxError("Incorrect syntax of switch-case statement.")
    return line_id


def check_break_flag(break_flag):
    """
    Function to check syntax.
    """
    if break_flag:
        return 0
    raise SyntaxError(
        "Control cannot fall through from one case label to another. "
        "'break' statement is required at the end of case block without "
        "'return' method."
    )
