from flask import Flask, request, redirect, url_for, render_template_string
from cs50 import SQL

app = Flask(__name__)
db = SQL("sqlite:///av.db")
db.execute('create table if not exists stock(itm_no int, name varchar(25), stock int, price int)')

INDEX_HTML = """
<h1>Store Stock Management</h1>
<ul>
  <li><a href="{{ url_for('insert_item') }}">Add Item</a></li>
  <li><a href="{{ url_for('display_items') }}">Display Items</a></li>
  <li><a href="{{ url_for('update_item') }}">Update Stock</a></li>
  <li><a href="{{ url_for('sale') }}">Sell Items</a></li>
</ul>
"""

INSERT_HTML = """
<h2>Add Item</h2>
<form method="post">
  Item Number: <input type="number" name="itm_no" required><br>
  Name: <input type="text" name="name" required><br>
  Stock: <input type="number" name="stock" required><br>
  Price: <input type="number" name="price" required><br>
  <input type="submit" value="Add">
</form>
<a href="{{ url_for('index') }}">Back</a>
{% if message %}<p>{{ message }}</p>{% endif %}
"""

DISPLAY_HTML = """
<h2>Items List</h2>
<table border="1">
  <tr><th>Item NO.</th><th>Name</th><th>Stock</th><th>Price</th></tr>
  {% for item in items %}
  <tr>
    <td>{{ item['itm_no'] }}</td>
    <td>{{ item['name'] }}</td>
    <td>{{ item['stock'] }}</td>
    <td>{{ item['price'] }}</td>
  </tr>
  {% endfor %}
</table>
<a href="{{ url_for('index') }}">Back</a>
"""

UPDATE_HTML = """
<h2>Update Stock</h2>
<form method="post">
  Item Number: <input type="number" name="itm_no" required><br>
  New Stock: <input type="number" name="stock" required><br>
  <input type="submit" value="Update">
</form>
<a href="{{ url_for('index') }}">Back</a>
{% if message %}<p>{{ message }}</p>{% endif %}
"""

SALE_HTML = """
<h2>Sell Multiple Items</h2>
<form method="post">
  Item Numbers (comma-separated): <input type="text" name="itm_nos" required><br>
  Quantities (comma-separated, matching order): <input type="text" name="quantities" required><br>
  <input type="submit" value="Sell">
</form>
<a href="{{ url_for('index') }}">Back</a>
{% if result %}<pre>{{ result }}</pre>{% endif %}
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/insert', methods=['GET', 'POST'])
def insert_item():
    message = ""
    if request.method == 'POST':
        ino = request.form['itm_no']
        iname = request.form['name']
        istock = request.form['stock']
        iprice = request.form['price']
        db.execute("insert into stock values (?, ?, ?, ?)", ino, iname, istock, iprice)
        message = "Item added successfully."
    return render_template_string(INSERT_HTML, message=message)

@app.route('/display')
def display_items():
    items = db.execute('select * from stock order by price desc')
    return render_template_string(DISPLAY_HTML, items=items)

@app.route('/update', methods=['GET', 'POST'])
def update_item():
    message = ""
    if request.method == 'POST':
        ino = request.form['itm_no']
        new_stock = request.form['stock']
        result = db.execute('update stock set stock = ? where itm_no = ?', new_stock, ino)
        if result is not None:
            message = "Stock updated."
        else:
            message = "Item not found."
    return render_template_string(UPDATE_HTML, message=message)

@app.route('/sale', methods=['GET', 'POST'])
def sale():
    result = ""
    if request.method == 'POST':
        itm_nos = request.form['itm_nos'].split(',')
        quantities = request.form['quantities'].split(',')
        total = 0
        messages = []
        if len(itm_nos) != len(quantities):
            result = "Item numbers and quantities count mismatch."
            return render_template_string(SALE_HTML, result=result)
        for ino, qty in zip(itm_nos, quantities):
            ino = ino.strip()
            try:
                qty = int(qty.strip())
            except ValueError:
                messages.append(f"Invalid quantity for item {ino}. Skipped.")
                continue
            items = db.execute('select * from stock where itm_no = ?', ino)
            if not items:
                messages.append(f"Item {ino} not found. Skipped.")
                continue
            item = items[0]
            if item['stock'] < qty:
                messages.append(f"Not enough stock for item {ino}. Available: {item['stock']}. Skipped.")
                continue
            db.execute('update stock set stock = stock - ? where itm_no = ?', qty, ino)
            subtotal = item['price'] * qty
            total += subtotal
            messages.append(f"Sold {qty} units of {item['name']} (Item {ino}) for {subtotal}.")
        messages.append(f"\nTotal amount for this sale: {total}")
        result = "\n".join(messages)
    return render_template_string(SALE_HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True)