import pytest
import os
import sys
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

def test_dashboard(client):
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert b'Dashboard' in rv.data

def test_expenses_page(client):
    """Test that the expenses page loads without error (verifying the macro fix)."""
    rv = client.get('/expenses')
    assert rv.status_code == 200
    assert b'Adicionar Novo' in rv.data
    # Check if the step attribute was rendered correctly
    assert b'step="0.01"' in rv.data
