from functools import reduce
 
 
# ---------------- Part 2 ----------------
 
def calculate_cart_total(discount_rate, *prices):
    """Apply the discount percent to every price and return the total as float."""
    factor = 1 - discount_rate / 100
    return float(sum(price * factor for price in prices))
 
 
def filter_and_sort_products(**products):
    """Keep products priced >= 100, return list of (name, price) sorted ascending by price."""
    expensive = filter(lambda item: item[1] >= 100, products.items())
    return sorted(expensive, key=lambda item: item[1])
 
 
# ---------------- Part 3 ----------------
 
def pair_students(names_list, scores_list):
    """Pair names with scores using zip, return a list of tuples."""
    return list(zip(names_list, scores_list))
 
 
def get_passed_students(paired_data, passing_score=60):
    """Keep only students whose score is >= passing_score."""
    return list(filter(lambda pair: pair[1] >= passing_score, paired_data))
 
 
def calculate_average_of_passed(passed_students):
    """Average score of the passed students using map and reduce."""
    if not passed_students:
        return 0.0
    scores = map(lambda pair: pair[1], passed_students)
    total = reduce(lambda acc, score: acc + score, scores, 0)
    return total / len(passed_students)
 
 
if __name__ == "__main__":
    print(calculate_cart_total(10, 100, 200, 300))  # 540.0
    print(filter_and_sort_products(laptop=2500, mouse=50, phone=800, cable=100))
 
    names = ["Ana", "Nino", "Luka", "Giorgi", "Mariam"]
    scores = [45, 82, 91, 38, 74]
 
    paired = pair_students(names, scores)
    passed = get_passed_students(paired)
    print(paired)
    print(passed)
    print(calculate_average_of_passed(passed))  # (82 + 91 + 74) / 3
 