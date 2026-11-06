import pytest

from src.triangle import InvalidTriangleException, Triangle, TriangleType


@pytest.fixture
def cut():
    return Triangle()


# ---------- Triângulos válidos ----------

def test_valid_scalene_triangle(cut):
    assert cut.classify(3, 4, 5) == TriangleType.ESCALENO


def test_valid_isosceles_triangle(cut):
    assert cut.classify(5, 5, 3) == TriangleType.ISOSCELES


def test_valid_equilateral_triangle(cut):
    assert cut.classify(4, 4, 4) == TriangleType.EQUILATERO


# ---------- Isósceles: permutação dos mesmos valores (3 CTs) ----------

@pytest.mark.parametrize("a, b, c", [
    (5, 5, 3),
    (5, 3, 5),
    (3, 5, 5),
])
def test_isosceles_permutations(cut, a, b, c):
    assert cut.classify(a, b, c) == TriangleType.ISOSCELES


# ---------- Um valor zero ----------

@pytest.mark.parametrize("a, b, c", [
    (0, 4, 5),
    (3, 0, 5),
    (3, 4, 0),
])
def test_one_side_zero_is_invalid(cut, a, b, c):
    with pytest.raises(InvalidTriangleException):
        cut.classify(a, b, c)


# ---------- Um valor negativo ----------

@pytest.mark.parametrize("a, b, c", [
    (-3, 4, 5),
    (3, -4, 5),
    (3, 4, -5),
])
def test_one_side_negative_is_invalid(cut, a, b, c):
    with pytest.raises(InvalidTriangleException):
        cut.classify(a, b, c)


# ---------- Soma de 2 lados IGUAL ao terceiro (um CT por permutação) ----------

@pytest.mark.parametrize("a, b, c", [
    (1, 2, 3),
    (1, 3, 2),
    (2, 1, 3),
    (2, 3, 1),
    (3, 1, 2),
    (3, 2, 1),
])
def test_sum_of_two_sides_equal_to_third_is_invalid(cut, a, b, c):
    with pytest.raises(InvalidTriangleException):
        cut.classify(a, b, c)


# ---------- Soma de 2 lados MENOR que o terceiro (um CT por permutação) ----------

@pytest.mark.parametrize("a, b, c", [
    (1, 2, 5),
    (1, 5, 2),
    (2, 1, 5),
    (2, 5, 1),
    (5, 1, 2),
    (5, 2, 1),
])
def test_sum_of_two_sides_less_than_third_is_invalid(cut, a, b, c):
    with pytest.raises(InvalidTriangleException):
        cut.classify(a, b, c)


# ---------- Os três valores iguais a zero ----------

def test_all_sides_zero_is_invalid(cut):
    with pytest.raises(InvalidTriangleException):
        cut.classify(0, 0, 0)


# ---------- Tipos inválidos (o programa lê valores inteiros) ----------

@pytest.mark.parametrize("a, b, c", [
    (3.5, 4, 5),
    ("3", 4, 5),
    (None, 4, 5),
    (True, 4, 5),
])
def test_non_integer_side_raises_type_error(cut, a, b, c):
    with pytest.raises(TypeError):
        cut.classify(a, b, c)
