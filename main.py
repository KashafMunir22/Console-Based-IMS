class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def authenticate(self, input_password):
        return self.password == input_password


class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, quantity):
        self.stock_quantity += quantity

    def update_details(self, name=None, category=None, price=None, stock_quantity=None):
        if name:
            self.name = name
        if category:
            self.category = category
        if price:
            self.price = price
        if stock_quantity:
            self.stock_quantity = stock_quantity


class InventoryManagementSystem:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.low_stock_threshold = 5

    def add_user(self, username, password, role):
        self.users[username] = User(username, password, role)

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.authenticate(password):
            print(f"Welcome, {username}!")
            return user
        else:
            print("Invalid username or password.")
            return None

    def add_product(self, product_id, name, category, price, stock_quantity):
        if product_id in self.products:
            print("Product ID already exists.")
        else:
            self.products[product_id] = Product(product_id, name, category, price, stock_quantity)
            print("Product added successfully.")

    def update_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        product = self.products.get(product_id)
        if product:
            product.update_details(name, category, price, stock_quantity)
            print("Product updated successfully.")
        else:
            print("Product not found.")

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            print("Product deleted successfully.")
        else:
            print("Product not found.")

    def view_products(self, filter_stock=False):
        if not self.products:
            print("No products available.")
            return
        for product in self.products.values():
            if filter_stock and product.stock_quantity > self.low_stock_threshold:
                continue
            print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                  f"Price: {product.price}, Stock: {product.stock_quantity}")

    def restock_product(self, product_id, quantity):
        product = self.products.get(product_id)
        if product:
            product.update_stock(quantity)
            print("Product restocked successfully.")
        else:
            print("Product not found.")

    def low_stock_warning(self):
        low_stock_found = False
        for product in self.products.values():
            if product.stock_quantity < self.low_stock_threshold:
                print(f"Low stock warning: {product.name} (ID: {product.product_id}) has only {product.stock_quantity} items left.")
                low_stock_found = True
        if not low_stock_found:
            print("No products with low stock.")


def main():
    ims = InventoryManagementSystem()

    # Add default users
    ims.add_user("admin", "admin123", "Admin")
    ims.add_user("user", "user123", "User")

    # Login process
    username = input("Enter username: ")
    password = input("Enter password: ")
    current_user = ims.login(username, password)

    if not current_user:
        return

    while True:
        print("\n1. View Products")
        if current_user.role == "Admin":
            print("2. Add Product")
            print("3. Update Product")
            print("4. Delete Product")
            print("5. Restock Product")

        print("6. Check Low Stock")
        print("7. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            ims.view_products()
        elif choice == "2" and current_user.role == "Admin":
            product_id = input("Enter Product ID: ")
            name = input("Enter Product Name: ")
            category = input("Enter Product Category: ")
            try:
                price = float(input("Enter Product Price: "))
                stock_quantity = int(input("Enter Stock Quantity: "))
                ims.add_product(product_id, name, category, price, stock_quantity)
            except ValueError:
                print("Invalid input. Price should be a number, and stock quantity should be an integer.")
        elif choice == "3" and current_user.role == "Admin":
            product_id = input("Enter Product ID: ")
            name = input("Enter New Name (leave blank to skip): ")
            category = input("Enter New Category (leave blank to skip): ")
            try:
                price = input("Enter New Price (leave blank to skip): ")
                stock_quantity = input("Enter New Stock Quantity (leave blank to skip): ")
                ims.update_product(
                    product_id,
                    name or None,
                    category or None,
                    float(price) if price else None,
                    int(stock_quantity) if stock_quantity else None
                )
            except ValueError:
                print("Invalid input. Price should be a number, and stock quantity should be an integer.")
        elif choice == "4" and current_user.role == "Admin":
            product_id = input("Enter Product ID to delete: ")
            ims.delete_product(product_id)
        elif choice == "5" and current_user.role == "Admin":
            product_id = input("Enter Product ID to restock: ")
            try:
                quantity = int(input("Enter Quantity to add: "))
                ims.restock_product(product_id, quantity)
            except ValueError:
                print("Invalid input. Quantity should be an integer.")
        elif choice == "6":
            ims.low_stock_warning()
        elif choice == "7":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice or permission denied.")


if __name__ == "__main__":
    main()
