
def unquote(string):
    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]
    return string
