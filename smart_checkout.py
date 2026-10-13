#saba rasmerchodii ?????
#  monacemta sheyvana 
cart_total = float(input("basket cost (gel): "))
user_status = input("status (regular / vip / admin): ").strip().lower()
has_promo_code = input("do you have promo code ? (yes/no): ").strip().lower() == "yes"
loyalty_points = int(input("points: "))
delivery_city = input("city to deliver : ").strip()
is_account_active = input("is account acctive ? (yes/no): ").strip().lower() == "yes"

# angarishis validacia 
if not is_account_active:
    print("account is blocked. order error.")

# kalatis minimaluri zgvari_
elif cart_total < 0:
    print("The cart total cannot be negative.")
elif cart_total == 0:
    print("The cart is empty. The order cannot be processed.")

else:
    # fasdaklebis sistema
    discount_percent = 0

    if user_status == "vip":
        discount_percent = 20
        if loyalty_points >= 500:
            discount_percent += 5  # sul 25%
    elif user_status == "regular":
        if has_promo_code or cart_total >= 150:
            discount_percent = 10
    elif user_status == "admin":
        discount_percent = 50
    else:
        print("Unknown status.")
        raise SystemExit

    discounted_total = cart_total * (1 - discount_percent / 100)

    # deliverys safasuri
    if delivery_city in ["tbilisi", "kutaisi", "batumi"]:
        if discounted_total >= 100:
            delivery_fee = 0
        else:
            delivery_fee = 5
    else:
        delivery_fee = 15  # regionebi

    final_total = discounted_total + delivery_fee

    # invoisis awkoba 

    print("\n===== invois =====")
    print(f"Initial cart price: {cart_total:.2f} gel")
    print(f"discount: {discount_percent}%")
    print(f"discounted prise: {discounted_total:.2f} gel")
    print(f"delivery price: {delivery_fee:.2f} gel")
    print(f"total price: {final_total:.2f} gel")
    print("order approved ")