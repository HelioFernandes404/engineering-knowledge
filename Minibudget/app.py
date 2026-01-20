from flask import Flask, render_template, request, redirect, url_for, flash
import db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta # Need to install python-dateutil if not available, or use simple math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_key_very_secret'
db.init_app(app)

# Constants for Dropdowns
CATEGORIES = ['Alimentação', 'Moradia', 'Transporte', 'Saúde', 'Lazer', 'Assinaturas', 'Outros']
PAYMENT_TYPES = ['Crédito', 'Débito', 'Pix', 'Dinheiro']

@app.context_processor
def inject_now():
    return {'now': datetime.now}

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # 1. Determine Month Context
    month_str = request.args.get('month')
    if not month_str:
        month_str = datetime.now().strftime('%Y-%m')
    
    try:
        current_date = datetime.strptime(month_str, '%Y-%m')
    except ValueError:
        current_date = datetime.now()
        month_str = current_date.strftime('%Y-%m')

    # Calculate Next/Prev for Navigation
    prev_month = (current_date - relativedelta(months=1)).strftime('%Y-%m')
    next_month = (current_date + relativedelta(months=1)).strftime('%Y-%m')
    
    # Dynamic Budget from DB
    MONTHLY_BUDGET = db.get_float_setting('monthly_budget', 3500.00)
    
    # Get expenses for selected month
    expenses = db.query_db(
        "SELECT * FROM expenses WHERE strftime('%Y-%m', expense_date) = ? ORDER BY expense_date DESC", 
        [month_str]
    )
    
    total_spent = sum(e['amount'] for e in expenses)
    remaining = MONTHLY_BUDGET - total_spent
    percentage = (total_spent / MONTHLY_BUDGET) * 100 if MONTHLY_BUDGET > 0 else 0
    
    # Group by Category for simple chart/list
    category_stats = {}
    for e in expenses:
        cat = e['category']
        category_stats[cat] = category_stats.get(cat, 0) + e['amount']
    
    return render_template(
        'dashboard.html',
        expenses=expenses[:5], # Last 5 transactions
        total_spent=total_spent,
        budget=MONTHLY_BUDGET,
        remaining=remaining,
        percentage=percentage,
        category_stats=category_stats,
        current_date=current_date,
        prev_month=prev_month,
        next_month=next_month
    )

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        monthly_budget = request.form['monthly_budget']
        db.set_setting('monthly_budget', monthly_budget)
        flash('Configurações atualizadas com sucesso!', 'success')
        return redirect(url_for('settings'))
    
    monthly_budget = db.get_setting('monthly_budget', default='3500.00')
    return render_template('settings.html', monthly_budget=monthly_budget)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    # Edit Mode Check
    edit_id = request.args.get('edit')
    edit_expense = None
    if edit_id:
        edit_expense = db.query_db('SELECT * FROM expenses WHERE id = ?', [edit_id], one=True)

    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']
        payment_type = request.form['payment_type']
        date = request.form['expense_date']
        expense_id = request.form.get('expense_id') # Hidden field for edit

        if expense_id:
            # Update Existing
            db.query_db(
                'UPDATE expenses SET description=?, amount=?, category=?, payment_type=?, expense_date=? WHERE id=?',
                [description, amount, category, payment_type, date, expense_id]
            )
            flash('Despesa atualizada com sucesso!', 'success')
        else:
            # Insert New
            db.query_db(
                'INSERT INTO expenses (description, amount, category, payment_type, expense_date) VALUES (?, ?, ?, ?, ?)',
                [description, amount, category, payment_type, date]
            )
            flash('Despesa adicionada com sucesso!', 'success')
            
        return redirect(url_for('expenses'))
        
    all_expenses = db.query_db("SELECT * FROM expenses ORDER BY expense_date DESC")
    
    return render_template(
        'expenses.html', 
        expenses=all_expenses,
        categories=CATEGORIES,
        payment_types=PAYMENT_TYPES,
        today=datetime.now().strftime('%Y-%m-%d'),
        edit_expense=edit_expense
    )

@app.route('/expenses/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    db.query_db('DELETE FROM expenses WHERE id = ?', [id])
    flash('Despesa removida.', 'neutral')
    return redirect(url_for('expenses'))

# Custom Filters for visual formatting
@app.template_filter('currency')
def currency_filter(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@app.template_filter('date_br')
def date_br_filter(value):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    return value.strftime('%d/%m/%Y')

@app.template_filter('month_br')
def month_br_filter(value):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y-%m') # Handle month string
            except ValueError:
                return value
    
    months = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    return f"{months[value.month]} {value.year}"

if __name__ == '__main__':
    app.run(debug=True, port=5000)