from Basilisk.main import compute


def test_simple():
    x = 3
    y = 4
    z = compute(x, y)
    assert z == x + y
