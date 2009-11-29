from model.style import Style

def test_default_style():
    assert Style.default() is not None
