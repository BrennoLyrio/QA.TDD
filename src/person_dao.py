import re

ERROR_NAME = "O nome deve ter ao menos 2 partes compostas somente por letras"
ERROR_AGE = "A idade deve estar no intervalo [1, 200]"
ERROR_EMAIL_REQUIRED = "A pessoa deve ter pelo menos um email associado"
ERROR_EMAIL_FORMAT = "O email deve estar no formato ____@____.____"

AGE_MIN = 1
AGE_MAX = 200

# ____@____.____ : cada parte com ao menos um caractere, sem espaços e
# com um único @ (o domínio pode ter mais pontos, ex.: fatec.sp.gov.br)
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")


class Email:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Person:

    def __init__(self, id, name, age, emails=None):
        self.id = id
        self.name = name
        self.age = age
        self.emails = emails if emails is not None else []


class PersonDAO:

    def __init__(self):
        self.persons = []

    def save(self, p):
        errors = self.is_valid_to_include(p)
        if errors:
            raise ValueError("; ".join(errors))
        self.persons.append(p)

    def is_valid_to_include(self, p):
        """Retorna a lista de erros de validação da pessoa (vazia se válida)."""
        if p is None:
            raise ValueError("A pessoa não pode ser None")

        errors = []

        if not self._is_valid_name(p.name):
            errors.append(ERROR_NAME)

        if not self._is_valid_age(p.age):
            errors.append(ERROR_AGE)

        if not p.emails:
            errors.append(ERROR_EMAIL_REQUIRED)
        elif not all(self._is_valid_email(email) for email in p.emails):
            errors.append(ERROR_EMAIL_FORMAT)

        return errors

    @staticmethod
    def _is_valid_name(name):
        if not isinstance(name, str):
            return False
        parts = name.split()
        return len(parts) >= 2 and all(part.isalpha() for part in parts)

    @staticmethod
    def _is_valid_age(age):
        if not isinstance(age, int) or isinstance(age, bool):
            return False
        return AGE_MIN <= age <= AGE_MAX

    @staticmethod
    def _is_valid_email(email):
        address = getattr(email, "name", None)
        return isinstance(address, str) and EMAIL_PATTERN.match(address) is not None
