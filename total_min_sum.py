total = 0
count = 0
minimum = None
maximum = None

while True:
    user_input = input("input a number  (or 'stop' for finish): ").strip()

    if user_input.lower() == "stop":
        break

    try:
        number = float(user_input)
    except ValueError:
        print("input only a number or  'stop'")
        continue

    total += number
    count += 1

    if minimum is None or number < minimum:
        minimum = number
    if maximum is None or number > maximum:
        maximum = number

while True:
    user_input = input("input number (or 'stop' for finish): ").strip()

    if user_input.lower() == "stop":
        break

    try:
        number = float(user_input)
    except ValueError:
        print("input only number to  'stop'")
        continue
