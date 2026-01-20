from flask import Flask, render_template, request, redirect, url_for, flash, g
import db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta # Need to install python-dateutil if not available, or use simple math

# Function to create and configure the Flask app
def create_app(config_object=None):
    app = Flask(__name__)

    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY='dev_key_very_secret', # Default key, should be overridden for production
        DATABASE='minibudget.sqlite', # Default database file
    )

    # Load environment-specific configuration if provided
    if config_object:
        app.config.from_object(config_object)
    
    # Initialize database with the app
    db.init_app(app)

    # Register context processor for global variables in templates
    @app.context_processor
    def inject_globals():
        return {
            'now': datetime.now,
            'current_app': app # Make app instance available in templates if needed
        }

    # --- Routes ---
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
        # Use get_float_setting directly, it handles default and conversion
        MONTHLY_BUDGET = db.get_float_setting('monthly_budget', 3500.00)
        
        # Get expenses for selected month
        expenses = db.query_db(
            "SELECT * FROM expenses WHERE strftime('%Y-%m', expense_date) = ? ORDER BY expense_date DESC", 
            [month_str]
        )
        
        total_spent = sum(e['amount'] for e in expenses)
        remaining = MONTHLY_BUDGET - total_spent
        percentage = (total_spent / MONTHLY_BUDGET) * 100 if MONTHLY_BUDGET > 0 else 0
        
        # --- COMPARATIVES & INSIGHTS ---

        # 1. Previous Month Comparison
        prev_expenses_sum = db.query_db(
            "SELECT SUM(amount) as total FROM expenses WHERE strftime('%Y-%m', expense_date) = ?", 
            [prev_month], one=True
        )['total']
        
        prev_month_total = prev_expenses_sum if prev_expenses_sum else 0.0
        
        delta_prev_val = total_spent - prev_month_total
        delta_prev_pct = 0
        if prev_month_total > 0:
            delta_prev_pct = ((total_spent - prev_month_total) / prev_month_total) * 100

        # 2. 3-Month Average (Historical Context)
        date_minus_3 = (current_date - relativedelta(months=3)).strftime('%Y-%m-01')
        date_current_start = current_date.strftime('%Y-%m-01')

        avg_stats = db.query_db(
            """
            SELECT COUNT(DISTINCT strftime('%Y-%m', expense_date)) as months_count, 
                   SUM(amount) as total_sum 
            FROM expenses 
            WHERE expense_date >= ? AND expense_date < ?
            """,
            [date_minus_3, date_current_start], one=True
        )
        
        avg_3_months = 0.0
        if avg_stats and avg_stats['months_count'] and avg_stats['months_count'] > 0:
            avg_3_months = avg_stats['total_sum'] / avg_stats['months_count']
        
        delta_avg_val = total_spent - avg_3_months

        # Trend Indicator logic
        trend = 'stable'
        if total_spent > (avg_3_months * 1.05): # > 5% higher
            trend = 'up'
        elif total_spent < (avg_3_months * 0.95): # < 5% lower (savings!)
            trend = 'down'

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
            next_month=next_month,
            # Insights
            prev_month_total=prev_month_total,
            delta_prev_val=delta_prev_val,
            delta_prev_pct=delta_prev_pct,
            avg_3_months=avg_3_months,
            delta_avg_val=delta_avg_val,
            trend=trend
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
                
            # Redirect to the main expenses page, not back to edit mode if it was a POST
            return redirect(url_for('expenses'))
            
        all_expenses = db.query_db("SELECT * FROM expenses ORDER BY expense_date DESC")
        
        return render_template(
            'expenses.html', 
            expenses=all_expenses,
            categories=['Alimentação', 'Moradia', 'Transporte', 'Saúde', 'Lazer', 'Assinaturas', 'Outros'], # Hardcoded for now
            payment_types=['Crédito', 'Débito', 'Pix', 'Dinheiro'], # Hardcoded for now
            today=datetime.now().strftime('%Y-%m-%d'),
            edit_expense=edit_expense
        )

    @app.route('/expenses/delete/<int:id>', methods=['POST'])
    def delete_expense(id):
        db.query_db('DELETE FROM expenses WHERE id = ?', [id])
        flash('Despesa removida.', 'neutral')
        return redirect(url_for('expenses'))

    # --- Custom Filters ---
    @app.template_filter('currency')
    def currency_filter(value):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @app.template_filter('date_br')
    def date_br_filter(value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return value # Return as-is if format is unexpected
        # Ensure value is a datetime object or compatible
        if isinstance(value, datetime):
            return value.strftime('%d/%m/%Y')
        return value # Return original value if not datetime or string

    @app.template_filter('month_br')
    def month_br_filter(value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                try: # Try parsing as YYYY-MM
                    value = datetime.strptime(value, '%Y-%m')
                except ValueError:
                    return value # Return as-is if format is unexpected
        
        months = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }
        if isinstance(value, datetime):
            return f"{months[value.month]} {value.year}"
        return value # Return original value if not datetime

    # --- CLI Commands ---
    # The init_db_command is added by db.init_app if it's called with an app that has a CLI
    # If using a test app with in-memory db, init_db is called directly in fixtures.
    # If running app.py directly, Flask CLI will find it via init_app.

    return app

# This part is for running the app directly (e.g., python app.py)
# It's not used by pytest fixtures
if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run(debug=True, port=5000)
