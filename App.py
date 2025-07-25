from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration (matches XAMPP/phpMyAdmin)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Web_app_database'

mysql = MySQL(app)

# Home - View all items
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inventory")
    items = cur.fetchall()
    cur.close()
    return render_template('index.html', items=items)

# Add item
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inventory (name, quantity, price) VALUES (%s, %s, %s)",
                    (name, quantity, price))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

# Update item
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        cur.execute("""
            UPDATE inventory
            SET name=%s, quantity=%s, price=%s
            WHERE id=%s
        """, (name, quantity, price, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM inventory WHERE id = %s", (id,))
    item = cur.fetchone()
    cur.close()
    return render_template('update_item.html', item=item)

# Delete item
@app.route('/delete/<int:id>')
def delete_item(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inventory WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)