from extensions import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)  # Unique product ID
    name = db.Column(db.String(255), nullable=False)  # Product name
    size = db.Column(db.String(255), nullable=False)  # Product size (added next to Name)
    stock_quantity = db.Column(db.Integer, nullable=False)  # Quantity in stock
    reorder_level = db.Column(db.Integer, nullable=False)  # Reorder threshold

    def __repr__(self):
        return f"<Product {self.name}, Size: {self.size}>"

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)  # Unique order ID
    customer_name = db.Column(db.String(255), nullable=False)  # Customer name
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.now())  # Order date
    status = db.Column(db.String(50), nullable=False)  # Order status (e.g., 'Pending')

    def __repr__(self):
        return f"<Order {self.id}: {self.status}>"

class Production(db.Model):
    __tablename__ = 'production'

    id = db.Column(db.Integer, primary_key=True)  # Unique production ID
    production_date = db.Column(db.Date, nullable=False)  # Date of production
    quantity = db.Column(db.Integer, nullable=False)  # Quantity produced

    def __repr__(self):
        return f"<Production {self.production_date}: {self.quantity}>"