scores = []

while True:
    value = input("Enter a score (0-10) or 'stop' to finish: ").strip()

    if value.lower() == "stop":
        break

    try:
        number = float(value)
    except ValueError:
        print("Please enter a valid number or 'stop'.")
        continue

    if 0 <= number <= 10:
        scores.append(number)
    else:
        print("The score must be between 0 and 10.")

if not scores:
    print("No scores were entered.")
else:
    minimum = min(scores)
    maximum = max(scores)
    average = sum(scores) / len(scores)

    print("\n" + "=" * 30)
    print(f"Minimum score: {minimum:g}")
    print(f"Maximum score: {maximum:g}")
    print(f"Class average: {average:.2f}")
    print("=" * 30)

    sorted_scores = sorted(scores)
    print("All scores (ascending): " + ", ".join(f"{s:g}" for s in sorted_scores))

    counts = {}
    for s in scores:
        counts[s] = counts.get(s, 0) + 1

    print("Score frequencies:")
    for score in sorted(counts):
        print(f"  {score:g} -> {counts[score]} time(s)")