import pytest

from src.salary_calculator import Employee, Role, SalaryCalculator


@pytest.fixture
def cut():
    return SalaryCalculator()


def make_employee(role, base_salary):
    return Employee("Joao Silva", "joao@email.com", base_salary, role)


# ---------- Regras por cargo (abaixo, no limite e acima do limiar) ----------

@pytest.mark.parametrize("role, base_salary, expected", [
    # DESENVOLVEDOR: >= 3000 -> 20% | < 3000 -> 10%
    (Role.DESENVOLVEDOR, 5000.00, 4000.00),
    (Role.DESENVOLVEDOR, 3000.00, 2400.00),
    (Role.DESENVOLVEDOR, 2999.99, 2699.99),
    (Role.DESENVOLVEDOR, 1000.00, 900.00),
    # DBA: >= 2000 -> 25% | < 2000 -> 15%
    (Role.DBA, 4000.00, 3000.00),
    (Role.DBA, 2000.00, 1500.00),
    (Role.DBA, 1999.99, 1699.99),
    (Role.DBA, 500.00, 425.00),
    # TESTADOR: >= 2000 -> 25% | < 2000 -> 15%
    (Role.TESTADOR, 4000.00, 3000.00),
    (Role.TESTADOR, 2000.00, 1500.00),
    (Role.TESTADOR, 1999.99, 1699.99),
    (Role.TESTADOR, 500.00, 425.00),
    # GERENTE: >= 5000 -> 30% | < 5000 -> 20%
    (Role.GERENTE, 8000.00, 5600.00),
    (Role.GERENTE, 5000.00, 3500.00),
    (Role.GERENTE, 4999.99, 3999.99),
    (Role.GERENTE, 2500.00, 2000.00),
])
def test_net_salary_by_role(cut, role, base_salary, expected):
    employee = make_employee(role, base_salary)
    assert cut.calculate(employee) == pytest.approx(expected, abs=0.01)


def test_zero_salary_results_in_zero(cut):
    assert cut.calculate(make_employee(Role.DESENVOLVEDOR, 0)) == 0


def test_result_is_rounded_to_two_decimals(cut):
    result = cut.calculate(make_employee(Role.DBA, 1234.57))
    assert result == round(result, 2)


def test_all_four_roles_are_distinct():
    assert len(Role) == 4
    assert Role.TESTADOR is not Role.DBA


# ---------- Funcionário ----------

def test_employee_keeps_its_data():
    employee = Employee("Maria Souza", "maria@email.com", 3500.0, Role.GERENTE)

    assert employee.name == "Maria Souza"
    assert employee.email == "maria@email.com"
    assert employee.base_salary == 3500.0
    assert employee.role == Role.GERENTE


@pytest.mark.parametrize("base_salary", [-0.01, -1000])
def test_negative_salary_raises_value_error(base_salary):
    with pytest.raises(ValueError):
        Employee("Joao Silva", "joao@email.com", base_salary, Role.DBA)


@pytest.mark.parametrize("base_salary", ["3000", None])
def test_non_numeric_salary_raises_type_error(base_salary):
    with pytest.raises(TypeError):
        Employee("Joao Silva", "joao@email.com", base_salary, Role.DBA)


@pytest.mark.parametrize("role", ["DESENVOLVEDOR", None, 1])
def test_invalid_role_raises_type_error(role):
    with pytest.raises(TypeError):
        Employee("Joao Silva", "joao@email.com", 3000.0, role)


def test_calculate_none_employee_raises_value_error(cut):
    with pytest.raises(ValueError):
        cut.calculate(None)
