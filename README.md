# Exercícios Práticos de TDD

Linguagem: **Python 3.12** · Framework de testes: **pytest** · Cobertura: **pytest-cov**

```
src/
  triangle.py            # Exercício 1 - Triângulo
  person_dao.py          # Exercício 2 - Person / Email / PersonDAO
  salary_calculator.py   # Exercício 3 - Calculadora de salário
test/
  triangle_test.py
  person_dao_test.py
  salary_calculator_test.py
```

# Installing Dependencies

Linux / macOS:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```


# Test Execution

Todos os exercícios, com cobertura (funciona em bash, PowerShell ou CMD):
```sh
python -m pytest test --cov=src --cov-report=term-missing
```

Um exercício por vez:
```sh
python -m pytest test/triangle_test.py          --cov=src.triangle          --cov-report=term-missing
python -m pytest test/person_dao_test.py        --cov=src.person_dao        --cov-report=term-missing
python -m pytest test/salary_calculator_test.py --cov=src.salary_calculator --cov-report=term-missing
```

Relatório HTML de cobertura (gerado em `htmlcov/index.html`):
```sh
python -m pytest test --cov=src --cov-report=html
```


# Exercício 1 - Triângulo

`Triangle().classify(a, b, c)` retorna `TriangleType.EQUILATERO`, `ISOSCELES` ou `ESCALENO`.
Lados que não formam triângulo lançam `InvalidTriangleException`; valores não inteiros lançam `TypeError`.

| Situação | Casos de teste (a, b, c) | Resultado esperado |
|---|---|---|
| Escaleno válido | (3, 4, 5) | ESCALENO |
| Isósceles válido | (5, 5, 3) | ISOSCELES |
| Equilátero válido | (4, 4, 4) | EQUILATERO |
| Isósceles - permutações | (5, 5, 3), (5, 3, 5), (3, 5, 5) | ISOSCELES |
| Um valor zero | (0, 4, 5), (3, 0, 5), (3, 4, 0) | InvalidTriangleException |
| Um valor negativo | (-3, 4, 5), (3, -4, 5), (3, 4, -5) | InvalidTriangleException |
| Soma de 2 lados = terceiro (todas as permutações) | (1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1) | InvalidTriangleException |
| Soma de 2 lados < terceiro (todas as permutações) | (1,2,5), (1,5,2), (2,1,5), (2,5,1), (5,1,2), (5,2,1) | InvalidTriangleException |
| Três valores iguais a zero | (0, 0, 0) | InvalidTriangleException |
| Valor não inteiro (extra) | (3.5, 4, 5), ("3", 4, 5), (None, 4, 5), (True, 4, 5) | TypeError |

Evidência de cobertura:
```
python -m pytest test/triangle_test.py --cov=src.triangle --cov-report=term-missing

Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
src\triangle.py      23      0   100%
-----------------------------------------------
TOTAL                23      0   100%
============================= 29 passed in 0.14s ==============================
```


# Exercício 2 - PersonDAO.isValidToInclude()

Implementação do diagrama de classes (`Person`, `Email`, `PersonDAO`). O método
`is_valid_to_include(p)` retorna uma **lista de erros** (vazia quando a pessoa é válida):

| Regra | Mensagem de erro |
|---|---|
| Nome com ao menos 2 partes, somente letras (acentos permitidos) | `ERROR_NAME` |
| Idade inteira no intervalo [1, 200] | `ERROR_AGE` |
| Pelo menos um `Email` associado | `ERROR_EMAIL_REQUIRED` |
| Cada `Email.name` no formato `____@____.____`, cada parte com ao menos 1 caractere | `ERROR_EMAIL_FORMAT` |

`save(p)` só armazena a pessoa se não houver erros; caso contrário lança `ValueError` com as mensagens.

Os testes cobrem os limites da idade (0, 1, 200, 201), nomes com 1 parte, números e símbolos,
emails sem `@`, sem `.`, com partes vazias, com dois `@` ou espaços, e o acúmulo de vários erros
na mesma pessoa.

Evidência de cobertura:
```
python -m pytest test/person_dao_test.py --cov=src.person_dao --cov-report=term-missing

Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src\person_dao.py      54      0   100%
-------------------------------------------------
TOTAL                  54      0   100%
============================= 47 passed in 0.19s ==============================
```


# Exercício 3 - Calculadora de Salário

`Employee(name, email, base_salary, role)` e `SalaryCalculator().calculate(employee)`, que retorna
o salário líquido arredondado em 2 casas. Cada `Role` guarda o próprio limiar e descontos:

| Cargo | Salário-base >= limiar | Salário-base < limiar |
|---|---|---|
| DESENVOLVEDOR | >= 3.000,00 → 20% | 10% |
| DBA | >= 2.000,00 → 25% | 15% |
| TESTADOR | >= 2.000,00 → 25% | 15% |
| GERENTE | >= 5.000,00 → 30% | 20% |

Para cada cargo há testes acima do limiar, **exatamente no limiar**, logo abaixo (limiar − 0,01) e
bem abaixo. Também são testados salário zero, salário negativo / não numérico e cargo inválido.

Evidência de cobertura:
```
python -m pytest test/salary_calculator_test.py --cov=src.salary_calculator --cov-report=term-missing

Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\salary_calculator.py      33      0   100%
--------------------------------------------------------
TOTAL                         33      0   100%
============================= 28 passed in 0.12s ==============================
```


# Cobertura geral

```
python -m pytest test --cov=src --cov-report=term-missing

Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\__init__.py                0      0   100%
src\person_dao.py             54      0   100%
src\salary_calculator.py      33      0   100%
src\triangle.py               23      0   100%
--------------------------------------------------------
TOTAL                        110      0   100%

============================= 104 passed in 0.36s =============================
```
