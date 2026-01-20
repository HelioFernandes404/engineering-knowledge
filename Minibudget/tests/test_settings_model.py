import pytest
import sys
import os
import sqlite3
import tempfile

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_get_set_budget_setting(client):
    """Testa se conseguimos ler e gravar o orçamento no banco."""
    with app.app_context():
        # 1. Tenta pegar o orçamento (deve retornar o padrão se não existir)
        # Nota: Estamos assumindo que vamos criar uma função get_setting
        from db import get_setting, set_setting
        
        initial_budget = get_setting('monthly_budget', default=3500.00)
        assert float(initial_budget) == 3500.00

        # 2. Atualiza o orçamento
        set_setting('monthly_budget', 5000.50)

        # 3. Verifica se atualizou
        new_budget = get_setting('monthly_budget')
        assert float(new_budget) == 5000.50
