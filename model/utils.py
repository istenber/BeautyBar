def unquote(string):
    if string.startswith('"') : string = string[1:]
    if string.endswith('"') : string = string[:-1]
    return string
