# ui.py
"""
UI/presentation layer – menu, printing, input prompts.
"""
from typing import Dict
from ticket import Ticket

def print_menu() -> None:
    print("\n" + "="*50)
    print("1. Create Ticket")
    print("2. Update Ticket")
    print("3. Reopen Ticket")
    print("4. Close Ticket")
    print("5. View All Tickets")
    print("6. Exit")
    print("="*50)

def get_choice() -> int:
    while True:
        try:
            choice = int(input("Enter your choice (1-6): ").strip())
            if 1 <= choice <= 6:
                return choice
            print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return 6

def display_tickets(ticket_dict: Dict[str, Ticket]) -> None:
    if not ticket_dict:
        print("No tickets available.")
        return

    sorted_tickets = sorted(
        ticket_dict.values(),
        key=lambda t: (
            *map(int, reversed(t.created_date.split('/'))),
            t.ticket_number
        )
    # Ensures correct chronological order across year boundaries
    )

    print("\n" + "-" * 120)
    for t in sorted_tickets:
        print(t)
    print("-" * 120)