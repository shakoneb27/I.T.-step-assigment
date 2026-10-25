"""Online shop inventory and customer analyzer (Dictionaries and Sets)."""

# Every product has the same set of characteristics: price, stock, year.
inventory = {
    "laptop": {"price": 2500, "stock": 5, "year": 2024},
    "smartphone": {"price": 1800, "stock": 12, "year": 2025},
    "headphones": {"price": 250, "stock": 0, "year": 2023},
    "keyboard": {"price": 120, "stock": 30, "year": 2022},
    "monitor": {"price": 900, "stock": 7, "year": 2024},
    "webcam": {"price": 150, "stock": 0, "year": 2021},
}

active_users = {"shakoneb27@mail.com", "nika_nika@mail.com", "sabaananidze@mail.com",
                "mari@mail.com", "giorgi@mail.com"}
vip_users = {"shakoneb27@mail.com", "mari@mail.com", "saba@mail.com",
             "anastasia@mail.com"}

LINE = "=" * 62
THIN = "-" * 62

def add_product(name, price, stock, year):
    "Add a new product. Returns True on success, False if it already exists."
    key = name.strip().lower()
    if not key or key in inventory:
        return False
    inventory[key] = {"price": price, "stock": stock, "year": year}
    return True

def update_stock(name, new_stock):
    """Update stock of an existing product. Returns True on success."""
    key = name.strip().lower()
    if key not in inventory:
        return False
    inventory[key]["stock"] = new_stock
    return True



def in_stock_products():
    "Return a dict with only the products whose stock is greater than 0."
    return {name: info for name, info in inventory.items() if info["stock"] > 0}

def most_expensive_product():
    "Return (name, info) of the most expensive product, or None if empty."
    if not inventory:
        return None
    name = max(inventory, key=lambda n: inventory[n]["price"])
    return name, inventory[name]

def total_inventory_value():
    "Sum of price * stock over all products."
    return sum(info["price"] * info["stock"] for info in inventory.values())


def print_table(products, title):  # Printing
    print(f"\n{title}")
    print(THIN)
    print(f"{'Product':<16}{'Price':>10}{'Stock':>8}{'Year':>8}{'Value':>14}")
    print(THIN)
    if not products:
        print("(no products)")
    for name, info in products.items():
        value = info["price"] * info["stock"]
        print(f"{name:<16}{info['price']:>10}{info['stock']:>8}"
              f"{info['year']:>8}{value:>14}")
    print(THIN)


def print_set(title, users):
    print(f"\n{title} ({len(users)}):")
    if not users:
        print("  (none)")
    for user in sorted(users):
        print(f"  - {user}")


def print_report():
    print("\n" + LINE)
    print("SHOP ANALYTICS REPORT".center(62))
    print(LINE)

    print_table(inventory, "FULL INVENTORY")
    print(f"Total inventory value: {total_inventory_value()}")

    print_table(in_stock_products(), "PRODUCTS IN STOCK (stock > 0)")

    top = most_expensive_product()
    if top:
        name, info = top
        print(f"\nMost expensive product: {name} (price: {info['price']})")

    print("\n" + LINE)
    print("CUSTOMER ANALYTICS".center(62))
    print(LINE)
    print_set("All unique users (union)", active_users | vip_users)
    print_set("Active AND VIP users (intersection)", active_users & vip_users)
    print_set("Active users who are NOT VIP (difference)",
              active_users - vip_users)
    print(LINE)


def read_number(prompt, cast=int, minimum=0):
    """Ask until the user enters a valid number >= minimum."""
    while True:
        raw = input(prompt).strip()
        try:
            value = cast(raw)
        except ValueError:
            print("Invalid number, try again.")
            continue
        if value < minimum:
            print(f"Value must be at least {minimum}.")
            continue
        return value

def menu():
    while True:
        print("\nMENU")
        print("  1) Add new product")
        print("  2) Update product stock")
        print("  3) Show report")
        print("  0) Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Product name: ")
            price = read_number("Price: ", float)
            stock = read_number("Stock: ", int)
            year = read_number("Release year: ", int, 1900)
            if add_product(name, price, stock, year):
                print("Product added.")
            else:
                print("Product already exists or name is empty.")
        elif choice == "2":
            name = input("Product name: ")
            if name.strip().lower() not in inventory:
                print("Product not found.")
                continue
            stock = read_number("New stock: ", int)
            update_stock(name, stock)
            print("Stock updated.")
        elif choice == "3":
            print_report()
        elif choice == "0":
            break
        else:
            print("Unknown option.")


def main():
    print_report()
    menu()
    print_report()


if __name__ == "__main__":
    main()