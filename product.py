class Product:
    store_name = "TechShop Georgia"
    currency = "GEL"
    total_products = 0

    def __init__(self, name, price, stock, category, discount=0):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.discount = discount
        Product.total_products += 1

    def get_info(self):
        return (
            f"Product: {self.name} | "
            f"Price: {self.price} {Product.currency} | "
            f"Stock: {self.stock} | "
            f"Category: {self.category} | "
            f"Discount: {self.discount}%"
        )

    def apply_discount(self, percent):
        if not 0 <= percent <= 100:
            print("Error: discount must be between 0 and 100.")
            return
        self.discount = percent
        print(f"Discount of {percent}% applied to '{self.name}'.")

    def update_stock(self, amount):
        new_stock = self.stock + amount
        if new_stock < 0:
            print(
                f"Warning: not enough stock for '{self.name}'. "
                f"Available: {self.stock}, requested change: {amount}."
            )
            return
        self.stock = new_stock
        print(f"Stock of '{self.name}' updated. New stock: {self.stock}.")

    def calculate_final_price(self):
        return self.price - (self.price * self.discount / 100)

    @classmethod
    def get_total_products_count(cls):
        return cls.total_products

if __name__ == "__main__":
    p1 = Product("Smartphone X", 1200, 15, "Electronics")
    p2 = Product("Wireless Headphones", 250, 30, "Electronics", discount=10)
    p3 = Product("Running Shoes", 180, 8, "Sportswear")

    print(p1.get_info())
    p1.apply_discount(15)
    print(f"Final price with discount: {p1.calculate_final_price()} {Product.currency}")

    print(p2.get_info())
    print(f"Final price with discount: {p2.calculate_final_price()} {Product.currency}")

    p3.update_stock(5)    
    p3.update_stock(-2)   
    p3.update_stock(-100) 
    print(p3.get_info())

    print(f"Total products created: {Product.get_total_products_count()}")