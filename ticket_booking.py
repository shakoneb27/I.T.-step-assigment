import re

TICKET_PRICE = 15  # price of one ticket in GEL


class InsufficientFundsError(ValueError):
    """Custom error raised when the paid amount is not enough."""


def main() -> None:
    try:
        # Question 1: how many tickets
        tickets_text = input("How many tickets would you like? ")
        tickets_numbers = re.findall(r"-?\d+(?:\.\d+)?", tickets_text)
        quantity = int(tickets_numbers[0])  # IndexError if no number, ValueError if not an int

        if quantity <= 0:
            raise ValueError("Ticket quantity must be at least 1")

        total = quantity * TICKET_PRICE
        print(f"One ticket costs {TICKET_PRICE:.2f} GEL. "
              f"Total for {quantity} ticket(s): {total:.2f} GEL.")

        # Question 2: how much the customer pays
        paid_text = input("How much are you paying? ")
        paid_numbers = re.findall(r"-?\d+(?:\.\d+)?", paid_text)
        paid = float(paid_numbers[0])  # IndexError if no number

        if paid < total:
            raise InsufficientFundsError(
                f"Insufficient funds (required {total:.2f}, provided {paid:.2f})"
            )

    except IndexError:
        print("Error: no number found in your input.")
    except InsufficientFundsError as e:  # must come before ValueError
        print(f"Booking rejected: {e}")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        change = paid - total
        print(f"Booking successful! Tickets: {quantity}, "
              f"total: {total:.2f} GEL, paid: {paid:.2f} GEL.")
        print(f"Your change: {change:.2f} GEL")
        print("We wish you a pleasant evening!")
    finally:
        print("[System]: Transaction attempt finished.")


if __name__ == "__main__":
    main()
