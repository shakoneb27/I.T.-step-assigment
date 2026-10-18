while True:
    try:
        height = int(input("input heigth of piramid (1-8): "))
    except ValueError:
        print("enter a number drom - 1 to 8.")
        continue

    if 1 <= height <= 8:
        break

    print("hig must be from 1 to 8.")

for row in range(1, height + 1):
    for _ in range(height - row):
        print(" ", end="")
    for _ in range(row):
        print("#", end="")
    print()
