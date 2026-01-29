# Estratégia de Testes

Esta página documenta a abordagem de testes do sistema, cobrindo configuração, fixtures, factories e cobertura de código.

---

## 🧪 Stack de Testes

| Ferramenta | Função | Versão |
| **Pytest** | Framework de testes | ~8.3.3 |
| **pytest-django** | Integração Pytest + Django | ~4.9.0 |
| **pytest-cov** | Relatório de cobertura | ~6.0.0 |
| **Factory Boy** | Geração de dados de teste | ~3.3.1 |
| **time-machine** | Simulação de data/hora | ~2.16.0 |

---

## 📂 Estrutura de Testes

```bash
#!/bin/bash
tests/
├── conftest.py                 # Fixtures globais
├── factories/                  # Factory Boy
│   ├── brand_factory.py
│   ├── category_factory.py
│   ├── product_factory.py
│   └── ...
├── api/                        # Testes de API (DRF)
│   └── v1/
│       ├── test_products.py
│       ├── test_inflows.py
│       └── ...
├── brands/                     # Testes unitários
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
└── integration/                # Testes de integração
    └── test_stock_flow.py
```

---

## ⚙️ Configuração Pytest

### pyproject.toml

```toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "app.settings"
python_files = ["test_*.py", "*_test.py"]
addopts = """
    --ds=app.settings
    --reuse-db
    --nomigrations
    --cov=.
    --cov-report=html
    --cov-report=term-missing:skip-covered
    -x
    --tb=short
"""

[tool.pytest_env]
# Força uso de SQLite em memória para testes
DATABASE_URL = "sqlite:///:memory:"
CELERY_TASK_ALWAYS_EAGER = "True"  # Executa tasks síncronas
```

### Flags Importantes

- `--reuse-db`: Reutiliza banco entre execuções (mais rápido)
- `--nomigrations`: Usa modelo direto (evita migrations lentas)
- `-x`: Para no primeiro erro
- `--cov`: Ativa relatório de cobertura

---

## 🏭 Factory Boy (Geração de Dados)

### Exemplo: ProductFactory

```python
# tests/factories/product_factory.py
import factory
from products.models import Product
from .brand_factory import BrandFactory
from .category_factory import CategoryFactory
from .product_model_factory import ProductModelFactory

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('name')
    product_model = factory.SubFactory(ProductModelFactory)
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker('text', max_nb_chars=200)
    serial_number = factory.Sequence(lambda n: f'SN-{n:05d}')
    cost_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    sell_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    quantity = factory.Faker('random_int', min=0, max=100)
```

### Uso nos Testes

```python
from tests.factories import ProductFactory

def test_product_creation():
    # Cria um produto com todas as dependências
    product = ProductFactory()
    assert product.id is not None
    assert product.quantity >= 0

def test_multiple_products():
    # Cria múltiplos produtos de uma vez
    products = ProductFactory.create_batch(5)
    assert len(products) == 5
```

---

## 📝 Categorias de Testes

### 1. Testes Unitários (Models)

**Propósito**: Validar lógica de negócio isolada.

```python
# tests/products/test_models.py
import pytest
from tests.factories import ProductFactory

@pytest.mark.django_db
class TestProductModel:
    def test_str_representation(self):
        product = ProductFactory(title="Notebook Dell")
        assert str(product) == "Notebook Dell"
    
    def test_default_quantity_is_zero(self):
        product = ProductFactory.build(quantity=None)
        product.save()
        assert product.quantity == 0
```

### 2. Testes de API (Request/Response)

**Propósito**: Validar endpoints REST.

```python
# tests/api/v1/test_products.py
import pytest
from rest_framework.test import APIClient
from tests.factories import ProductFactory, UserFactory

@pytest.mark.django_db
class TestProductAPI:
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
    
    def test_list_products(self):
        ProductFactory.create_batch(3)
        response = self.client.get('/api/v1/products/')
        assert response.status_code == 200
        assert len(response.data['results']) == 3
    
    def test_create_product_requires_auth(self):
        self.client.logout()
        response = self.client.post('/api/v1/products/', {})
        assert response.status_code == 401
```

### 3. Testes de Integração (Fluxo Completo)

**Propósito**: Validar interação entre múltiplos componentes.

```python
# tests/integration/test_stock_flow.py
import pytest
from tests.factories import ProductFactory, InflowFactory

@pytest.mark.django_db
class TestStockFlow:
    def test_inflow_updates_quantity(self):
        """Testa se signal de Inflow atualiza estoque."""
        product = ProductFactory(quantity=10)
        
        # Registra uma entrada
        InflowFactory(product=product, quantity=5)
        
        # Verifica se saldo foi atualizado
        product.refresh_from_db()
        assert product.quantity == 15
```

---

## 🕐 Time-Machine (Simulação de Tempo)

```python
import time_machine
from datetime import datetime

@time_machine.travel("2025-12-31 23:59:59")
def test_end_of_year_report():
    """Testa relatório de fim de ano."""
    # O sistema pensa que é 31/12/2025
    assert datetime.now().year == 2025
```

---

## 📊 Cobertura de Código

### Executar com Relatório

```bash
# Rodar testes com cobertura
uv run pytest

# Abrir relatório HTML
uv run python -m http.server --directory htmlcov 8080
```

### Targets de Cobertura

| Componente | Target | Atual |
| Models | 100% | ~95% |
| Views | 90% | ~88% |
| Serializers | 95% | ~92% |
| Logic/Services | 95% | ~90% |
| **Global** | **90%** | **~89%** |

---

## 🔍 Fixtures Globais (conftest.py)

```python
# tests/conftest.py
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Cliente autenticado para APIs."""
    return APIClient()

@pytest.fixture
def authenticated_user(db):
    """Usuário autenticado."""
    from tests.factories import UserFactory
    return UserFactory()

@pytest.fixture
def admin_client(admin_user):
    """Cliente com usuário admin."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
```

---

## 🚀 Executando Testes

### Comandos Principais

```bash
# Todos os testes
uv run pytest

# Apenas um arquivo
uv run pytest tests/products/test_models.py

# Apenas um teste específico
uv run pytest tests/products/test_models.py::test_product_creation

# Com output verboso
uv run pytest -v

# Parar no primeiro erro
uv run pytest -x

# Ver print() statements
uv run pytest -s
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci-cd.yml
- name: Run Tests
  run: |
    uv run pytest --cov --cov-report=xml
    
- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage.xml
```

---

## 🛠️ Debugging de Testes

### Usar Debugger

```python
import pytest

def test_something():
    breakpoint()  # Para execução aqui
    # ou
    import pdb; pdb.set_trace()
```

### Ver Queries SQL

```python
from django.test.utils import override_settings
from django.db import connection

@override_settings(DEBUG=True)
def test_with_sql_debug():
    # Suas queries...
    print(connection.queries)
```

---

## ✅ Boas Práticas

1. **Independência**: Cada teste deve rodar isoladamente
2. **Fixtures**: Use factories em vez de criar objetos manualmente
3. **Nomenclatura**: `test_<acão>_<resultado_esperado>`
4. **AAA Pattern**: Arrange, Act, Assert
5. **Coverage**: Mantenha acima de 85%
6. **Velocidade**: Suite completa deve rodar em < 2 minutos

```python
# ✅ BOM
def test_outflow_reduces_quantity():
    # Arrange
    product = ProductFactory(quantity=10)
    
    # Act
    OutflowFactory(product=product, quantity=3)
    
    # Assert
    product.refresh_from_db()
    assert product.quantity == 7

# ❌ RUIM (vários asserts não relacionados)
def test_everything():
    assert 1 + 1 == 2
    assert "foo" != "bar"
    # ...
```
