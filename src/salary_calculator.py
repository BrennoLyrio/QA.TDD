from enum import Enum


class Role(Enum):
    # (rótulo, limiar do salário-base, desconto se >= limiar, desconto se < limiar)
    # O rótulo garante valores únicos: sem ele DBA e TESTADOR viram aliases no Enum.
    DESENVOLVEDOR = ("Desenvolvedor", 3000.00, 0.20, 0.10)
    DBA = ("DBA", 2000.00, 0.25, 0.15)
    TESTADOR = ("Testador", 2000.00, 0.25, 0.15)
    GERENTE = ("Gerente", 5000.00, 0.30, 0.20)

    def __init__(self, label, threshold, high_discount, low_discount):
        self.label = label
        self.threshold = threshold
        self.high_discount = high_discount
        self.low_discount = low_discount

    def discount_for(self, base_salary):
        if base_salary >= self.threshold:
            return self.high_discount
        return self.low_discount


class Employee:

    def __init__(self, name, email, base_salary, role):
        if not isinstance(base_salary, (int, float)) or isinstance(base_salary, bool):
            raise TypeError(f"Salário-base inválido: {base_salary!r}")
        if base_salary < 0:
            raise ValueError("O salário-base não pode ser negativo")
        if not isinstance(role, Role):
            raise TypeError(f"Cargo inválido: {role!r}")

        self.name = name
        self.email = email
        self.base_salary = base_salary
        self.role = role


class SalaryCalculator:

    def calculate(self, employee):
        """Retorna o salário líquido do funcionário conforme a regra do cargo."""
        if employee is None:
            raise ValueError("O funcionário não pode ser None")

        discount = employee.role.discount_for(employee.base_salary)
        return round(employee.base_salary * (1 - discount), 2)
