import re

import pytest

from src.person_dao import (
    ERROR_AGE,
    ERROR_EMAIL_FORMAT,
    ERROR_EMAIL_REQUIRED,
    ERROR_NAME,
    Email,
    Person,
    PersonDAO,
)


@pytest.fixture
def cut():
    return PersonDAO()


def make_person(name="Joao Silva", age=30, emails=None):
    if emails is None:
        emails = [Email(1, "joao@email.com")]
    return Person(1, name, age, emails)


# ---------- Pessoa válida ----------

def test_valid_person_has_no_errors(cut):
    assert cut.is_valid_to_include(make_person()) == []


def test_result_is_a_list(cut):
    assert isinstance(cut.is_valid_to_include(make_person()), list)


# ---------- Nome: ao menos 2 partes, somente letras ----------

@pytest.mark.parametrize("name", [
    "Joao Silva",
    "Maria da Silva Souza",
    "José Conceição",          # letras acentuadas são letras
    "  Ana   Paula  ",         # espaços extras não criam partes vazias
])
def test_valid_names(cut, name):
    assert ERROR_NAME not in cut.is_valid_to_include(make_person(name=name))


@pytest.mark.parametrize("name", [
    "Joao",            # só 1 parte
    "",                # vazio
    "   ",             # só espaços
    "Joao S1lva",      # contém número
    "Joao Silva!",     # contém símbolo
    "Joao-Pedro",      # hífen não é letra e é 1 parte só
    None,
    123,
])
def test_invalid_names(cut, name):
    assert ERROR_NAME in cut.is_valid_to_include(make_person(name=name))


# ---------- Idade no intervalo [1, 200] ----------

@pytest.mark.parametrize("age", [1, 2, 100, 199, 200])
def test_valid_ages(cut, age):
    assert ERROR_AGE not in cut.is_valid_to_include(make_person(age=age))


@pytest.mark.parametrize("age", [0, -1, 201, 1000, 30.5, "30", None, True])
def test_invalid_ages(cut, age):
    assert ERROR_AGE in cut.is_valid_to_include(make_person(age=age))


# ---------- Pelo menos um Email associado ----------

def test_person_without_emails_is_invalid(cut):
    assert ERROR_EMAIL_REQUIRED in cut.is_valid_to_include(make_person(emails=[]))


def test_person_with_none_emails_is_invalid(cut):
    person = make_person()
    person.emails = None
    assert ERROR_EMAIL_REQUIRED in cut.is_valid_to_include(person)


def test_person_with_many_valid_emails_is_valid(cut):
    emails = [Email(1, "a@b.c"), Email(2, "joao.silva@empresa.com.br")]
    assert cut.is_valid_to_include(make_person(emails=emails)) == []


# ---------- Formato do Email: ____@____.____ ----------

@pytest.mark.parametrize("address", [
    "a@b.c",
    "joao@email.com",
    "joao.silva@fatec.sp.gov.br",
])
def test_valid_email_formats(cut, address):
    person = make_person(emails=[Email(1, address)])
    assert ERROR_EMAIL_FORMAT not in cut.is_valid_to_include(person)


@pytest.mark.parametrize("address", [
    "",
    "joaoemail.com",     # sem @
    "@email.com",        # parte antes do @ vazia
    "joao@.com",         # parte entre @ e . vazia
    "joao@email.",       # parte depois do . vazia
    "joao@email",        # sem .
    "joao@@email.com",   # dois @
    "jo ao@email.com",   # espaço
    None,
])
def test_invalid_email_formats(cut, address):
    person = make_person(emails=[Email(1, address)])
    assert ERROR_EMAIL_FORMAT in cut.is_valid_to_include(person)


def test_one_invalid_email_among_valid_ones_is_reported(cut):
    emails = [Email(1, "joao@email.com"), Email(2, "invalido")]
    assert cut.is_valid_to_include(make_person(emails=emails)) == [ERROR_EMAIL_FORMAT]


# ---------- Vários erros ao mesmo tempo ----------

def test_returns_all_errors_together(cut):
    person = make_person(name="Joao", age=0, emails=[])
    errors = cut.is_valid_to_include(person)

    assert errors == [ERROR_NAME, ERROR_AGE, ERROR_EMAIL_REQUIRED]


def test_none_person_raises_value_error(cut):
    with pytest.raises(ValueError):
        cut.is_valid_to_include(None)


# ---------- save() ----------

def test_save_valid_person(cut):
    person = make_person()
    cut.save(person)
    assert person in cut.persons


def test_save_invalid_person_raises_and_does_not_store(cut):
    person = make_person(age=0)
    with pytest.raises(ValueError, match=re.escape(ERROR_AGE)):
        cut.save(person)
    assert cut.persons == []
