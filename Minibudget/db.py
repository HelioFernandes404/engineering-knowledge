import sqlite3
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'minibudget.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv

def get_setting(key, default=None):
    """Retrieve a setting value by key."""
    row = query_db('SELECT value FROM settings WHERE key = ?', [key], one=True)
    return row['value'] if row else default

def get_float_setting(key, default=0.0):
    """Retrieve a setting value as float, handling conversion errors."""
    val = get_setting(key)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default

def set_setting(key, value):
    """Set or update a setting value."""
    # SQLite UPSERT syntax (requires newer SQLite) or INSERT OR REPLACE
    query_db('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', [key, str(value)])

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
