"""
This module file supports basic functions from stdio.h library
"""

from .utils import definition

@definition(return_type='int', arg_types=None)
def printf(*args):
    """ basic printf function
    example:
        printf("%d %d", 1, 2);
    """
    fmt, *params = args
    fmt = fmt.replace('\\n', '\n')
    message = fmt % tuple(params)
    result = len(message)
    print(message, end='')
    return result

@definition(return_type='int', arg_types=None)
def scanf(*args):
    """ basic printf function
        example:
            scanf("%d %d", 'a', 'b');
        """

    import re
    def cast(flag):
        if flag[-1] == 'd':
            return int
        raise Exception('You are not allowed to use \'{}\' other type'.format(flag))

    fmt, *params = args
    fmt = re.sub(r'\s+', '', fmt)
    all_flags = re.findall('%[^%]*[dfi]', fmt)
    if len(all_flags) != len(params):
        raise Exception('Format of scanf function takes {} positional arguments but {} were given'.format(
            len(all_flags),
            len(params)
        ))
    elements = []
    while len(elements) < len(all_flags):
        str = input()
        elements.extend(str.split())
    for flag, param, val in zip(all_flags, params, elements):
        memory[param] = cast(flag)(val)
    return len(elements)