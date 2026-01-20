import pytest
import sys
import os

# --- PATH CONFIGURATION ---
# Ensure the project root is in sys.path for module imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import create_app and db from app.py and db.py respectively
from app import create_app, db

# The 'client' fixture will now be provided by tests/conftest.py

def test_dashboard(client):
    """Test dashboard page loads correctly."""
    rv = client.get('/dashboard')
    assert rv.status_code == 200
    assert b'Vis\xc3\xa3o Geral' in rv.data # Check for "Visão Geral"

def test_expenses_page(client):
    """Test that the expenses page loads without error and form elements are present."""
    rv = client.get('/expenses')
    assert rv.status_code == 200
    assert b'Novo Lan\xc3\xa7amento' in rv.data # Check for "Novo Lançamento" in bytes
    # Check if the step attribute was rendered correctly for amount input
    assert b'step="0.01"' in rv.data