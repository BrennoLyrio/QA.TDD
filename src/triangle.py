from enum import Enum


class InvalidTriangleException(Exception):
    pass


class TriangleType(Enum):
    EQUILATERO = "equilátero"
    ISOSCELES = "isósceles"
    ESCALENO = "escaleno"


class Triangle:

    def classify(self, a, b, c):
        """Recebe três lados inteiros e informa o tipo do triângulo.
        Lança InvalidTriangleException se os lados não formam um triângulo."""
        sides = (a, b, c)

        for side in sides:
            # bool é subclasse de int, por isso a checagem explícita
            if not isinstance(side, int) or isinstance(side, bool):
                raise TypeError(f"Lado inválido (deve ser inteiro): {side!r}")

        if any(side <= 0 for side in sides):
            raise InvalidTriangleException("Todos os lados devem ser maiores que zero")

        # a soma de dois lados tem que ser maior que o terceiro lado
        if a + b <= c or a + c <= b or b + c <= a:
            raise InvalidTriangleException(
                "A soma de dois lados deve ser maior que o terceiro lado"
            )

        distinct_sides = len(set(sides))
        if distinct_sides == 1:
            return TriangleType.EQUILATERO
        if distinct_sides == 2:
            return TriangleType.ISOSCELES
        return TriangleType.ESCALENO
