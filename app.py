from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize database
DATABASE = 'transactions.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            transaction_type TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )''')
    conn.close()

# Route: Home (Display All Transactions)
@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = cursor.fetchall()
    return render_template('index.html', transactions=transactions)

# Route: Create Transaction
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        amount = request.form['amount']
        transaction_type = request.form['transaction_type']
        description = request.form['description']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transactions (amount, transaction_type, description, date) VALUES (?, ?, ?, ?)",
                           (amount, transaction_type, description, date))
        return redirect(url_for('index'))
    return render_template('form.html', transaction=None)

# Route: Edit Transaction
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        amount = request.form['amount']
        transaction_type = request.form['transaction_type']
        description = request.form['description']
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE transactions SET amount=?, transaction_type=?, description=? WHERE id=?",
                           (amount, transaction_type, description, id))
        return redirect(url_for('index'))
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id=?", (id,))
        transaction = cursor.fetchone()
    return render_template('form.html', transaction=transaction)

# Route: Delete Transaction
@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id=?", (id,))
    return redirect(url_for('index'))

# API Endpoints
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
    return jsonify(transactions)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
