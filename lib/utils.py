
__all__ = ["darker_color", "lighter_color"]

def _darker(part, amount):
    try:
        c = int(part, 16)
    except ValueError:
        # error
        return "ff"
    c -= amount
    if c < 0:
        return "00"
    elif c > 255:
        return "ff"
    elif c < 16:
        return "0" + hex(c)[2:3]
    else:
        return hex(c)[2:4]

def darker_color(color, amount):
    """ make rrggbb -color darker """
    return (_darker(color[0:2], amount) +
            _darker(color[2:4], amount) +
            _darker(color[4:6], amount))

def lighter_color(color, amount):
    """ make rrggbb -color lighter """
    return (_darker(color[0:2], -amount) +
            _darker(color[2:4], -amount) +
            _darker(color[4:6], -amount))
