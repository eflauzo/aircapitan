
from aircapitan.instruments.learn_simple import eng2norm


def test_eng2norm():
    assert eng2norm(0.0, (-3.14, 3.14)) == 0.0
    assert eng2norm(-3.14, (-3.14, 3.14)) == -1.0
    assert eng2norm(3.14, (-3.14, 3.14)) == 1.0

    assert eng2norm(0.0, (-100.0, 100.0)) == 0.0
    assert eng2norm(0.0, (-1.0, 1.0)) == 0.0
    assert eng2norm(1.0, (-1.0, 1.0)) == 1.0
    assert eng2norm(-1.0, (-1.0, 1.0)) == -1.0
