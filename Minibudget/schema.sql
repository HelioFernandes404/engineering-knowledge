DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS settings;

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL, -- 'Alimentação', 'Transporte', 'Lazer', 'Contas', 'Outros'
    payment_type TEXT NOT NULL, -- 'Cartão', 'Dinheiro', 'Pix'
    expense_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);