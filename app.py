from flask import Flask, render_template, request, Response
from extensions import db
from models import Product
import csv

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Paper%40123@localhost/stretch_film_system'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create tables if they don't already exist
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return "Flask app is running successfully!"

# Route to render the Add Product form
@app.route('/add-product-form', methods=['GET'])
def add_product_form():
    return render_template('add_product.html')

# Route to handle form submission and add a product to the database
@app.route('/submit-product', methods=['POST'])
def submit_product():
    name = request.form['name']
    size = request.form['size']
    stock_quantity = int(request.form['quantity'])
    reorder_level = int(request.form['reorder_level'])

    new_product = Product(name=name, size=size, stock_quantity=stock_quantity, reorder_level=reorder_level)
    db.session.add(new_product)
    db.session.commit()

    return f"Product '{name}' (Size: {size}) added successfully!"

# Route to display all products
@app.route('/products', methods=['GET'])
def view_products():
    products = Product.query.all()
    product_list = [
        f"""
        {product.id}: {product.name} (Size: {product.size}, Quantity: {product.stock_quantity}, Reorder Level: {product.reorder_level})
        - <a href="/edit-product/{product.id}">Edit</a>
        - <a href="/confirm-delete/{product.id}">Delete</a>
        """
        for product in products
    ]
    return "<br>".join(product_list)

# Route to render the Edit Product form
@app.route('/edit-product/<int:id>', methods=['GET'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    return render_template('edit_product.html', product=product)

# Route to handle product updates
@app.route('/update-product/<int:id>', methods=['POST'])
def update_product(id):
    product = Product.query.get_or_404(id)
    product.name = request.form['name']
    product.size = request.form['size']
    product.stock_quantity = int(request.form['quantity'])
    product.reorder_level = int(request.form['reorder_level'])

    db.session.commit()

    return f"Product '{product.name}' (Size: {product.size}) updated successfully!"

# Route to confirm deletion
@app.route('/confirm-delete/<int:id>', methods=['GET'])
def confirm_delete(id):
    product = Product.query.get_or_404(id)
    return render_template('confirm_delete.html', product=product)

# Route to delete a product
@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return f"Product '{product.name}' deleted successfully!"

# Route to render the Search Products form
@app.route('/search-products', methods=['GET'])
def search_products():
    return render_template('search_products.html')

# Route to display search results
@app.route('/search-results', methods=['GET'])
def search_results():
    search_query = request.args.get('search_query', '').lower()
    results = Product.query.filter(
        (Product.name.ilike(f'%{search_query}%')) |
        (Product.size.ilike(f'%{search_query}%'))
    ).all()
    result_list = [
        f"{product.id}: {product.name} (Size: {product.size}, Quantity: {product.stock_quantity}, Reorder Level: {product.reorder_level})"
        for product in results
    ]
    return "<br>".join(result_list) if results else "No products found matching your search."

# Route to display products with pagination
@app.route('/paginated-products', methods=['GET'])
def paginated_products():
    page = request.args.get('page', 1, type=int)  # Current page number
    per_page = 5  # Products per page
    paginated_products = Product.query.paginate(page=page, per_page=per_page)  # Paginated query
    product_list = [
        f"{product.id}: {product.name} (Size: {product.size}, Quantity: {product.stock_quantity}, Reorder Level: {product.reorder_level})"
        for product in paginated_products.items
    ]
    navigation = f"""
        {'<a href="?page=' + str(paginated_products.prev_num) + '">Previous</a>' if paginated_products.has_prev else ''}
        {'<a href="?page=' + str(paginated_products.next_num) + '">Next</a>' if paginated_products.has_next else ''}
    """
    return "<br>".join(product_list) + "<br>" + navigation

# Route to export products to CSV
@app.route('/export-products', methods=['GET'])
def export_products():
    products = Product.query.all()
    csv_data = [["ID", "Name", "Size", "Stock Quantity", "Reorder Level"]]  # Header row
    csv_data.extend([
        [product.id, product.name, product.size, product.stock_quantity, product.reorder_level]
        for product in products
    ])
    
    # Prepare the CSV file for download
    def generate_csv():
        for row in csv_data:
            yield ",".join(map(str, row)) + "\n"
    
    return Response(generate_csv(), mimetype="text/csv", headers={
        "Content-Disposition": "attachment; filename=products.csv"
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)