import math

import pytest

from euclid.dim2 import Vector, Path, get_unit_vector

v = Vector(1, 2)


def test_vector():
    assert v.x == 1
    assert v.y == 2
    assert v.norm == math.sqrt(5)
    assert v.angle == pytest.approx(1.107148)


def test_vector_operations():
    assert v == Vector(1, 2)
    assert v != Vector(1, 1)

    assert v - Vector(1, 1) == Vector(0, 1)


def test_unit_vector():
    u = get_unit_vector(v)
    assert u.x == v.x / v.norm
    assert u.norm == pytest.approx(1)


def test_path():
    p = Path(start=Vector(0, 0),
             end=Vector(3, 4))
    assert p.v.norm / p.u.norm == 5

    assert Path(start=Vector(0, 0),
                end=Vector(0, 4)).get_vectors() == [Vector(0, 0),
                                                    Vector(0, 1),
                                                    Vector(0, 2),
                                                    Vector(0, 3),
                                                    Vector(0, 4)]

    assert Path(start=Vector(0, 4),
                end=Vector(0, 0)).get_vectors() == [Vector(0, 4),
                                                    Vector(0, 3),
                                                    Vector(0, 2),
                                                    Vector(0, 1),
                                                    Vector(0, 0)]
