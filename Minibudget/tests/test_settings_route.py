import pytest
import sys
import os
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

def test_settings_page_loads(client):
    rv = client.get('/settings')
    assert rv.status_code == 200
    assert b'Configura' in rv.data

def test_update_budget(client):
    # 1. Update budget
    rv = client.post('/settings', data={'monthly_budget': '4200.00'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'atualizadas' in rv.data or b'sucesso' in rv.data

    # 2. Check if reflected in dashboard
    rv = client.get('/dashboard')
    assert b'4.200,00' in rv.data
