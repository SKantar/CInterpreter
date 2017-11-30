def printf(*args):
    fmt, *params = args
    print(fmt % tuple(params))

def scanf(*args):
    import re
    fmt, *params = args
    fmt = re.sub(r'\s+', '', fmt)
    all_flags = re.findall('%l?[dfi]', fmt)
    print(test)

scanf("%d %d");
