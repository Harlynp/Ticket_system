# main.py
"""
Application entry point – lifecycle, persistence, error handling.
"""
import json
import logging
from pathlib import Path
from typing import Dict, Tuple
from ticket import Ticket, create_ticket, update_ticket, reopen_ticket, close_ticket
from ui import print_menu, get_choice, display_tickets
from config import TICKETS_FILE, COUNTER_FILE, DATA_DIR, DEFAULT_COUNTER

log = logging.getLogger(__name__)

def load_data() -> Tuple[Dict[str, Ticket], int]:
    ticket_dict: Dict[str, Ticket] = {}
    counter = DEFAULT_COUNTER

    # Load tickets
    if TICKETS_FILE.exists():
        try:
            with open(TICKETS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    t = Ticket(item["ticket_number"], item["username"], item["description"])
                    t.status = item["status"]
                    t.created_date = item["created_date"]
                    t.updated_date = item["updated_date"]
                    ticket_dict[t.ticket_number] = t
            log.info(f"Loaded {len(ticket_dict)} ticket(s).")
        except json.JSONDecodeError as e:
            log.error(f"Corrupted JSON in {TICKETS_FILE}: {e}")
    # Continue with empty dict – prevents total failure
        except PermissionError as e:
            log.error(f"Permission denied: {e}")
        except Exception as e:
            log.exception(f"Unexpected load error: {e}")

    # Load counter
    if COUNTER_FILE.exists():
        try:
            with open(COUNTER_FILE, "r") as f:
                counter = max(int(f.read().strip()), DEFAULT_COUNTER)
        except ValueError:
            log.warning("Invalid counter value. Using default.")
        except PermissionError as e:
            log.error(f"Permission denied reading counter: {e}")
        except Exception as e:
            log.exception(f"Error reading counter: {e}")

    return ticket_dict, counter

def save_data(ticket_dict: Dict[str, Ticket], counter: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        data = [vars(t) for t in ticket_dict.values()]
        with open(TICKETS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        with open(COUNTER_FILE, "w") as f:
            f.write(str(counter))
    except PermissionError as e:
        log.error(f"Permission denied writing data: {e}")
    except Exception as e:
        log.exception(f"Failed to save data: {e}")

def main() -> None:
    ticket_dict, ticket_counter = load_data()
    print("Welcome to IT Ticketing System")

    while True:
        print_menu()
        choice = get_choice()

        try:
            if choice == 1:
                if create_ticket(ticket_dict, ticket_counter):
                    ticket_counter += 1
                    save_data(ticket_dict, ticket_counter)
            elif choice == 2:
                update_ticket(ticket_dict)
                save_data(ticket_dict, ticket_counter)
            elif choice == 3:
                reopen_ticket(ticket_dict)
                save_data(ticket_dict, ticket_counter)
            elif choice == 4:
                close_ticket(ticket_dict)
                save_data(ticket_dict, ticket_counter)
            elif choice == 5:
                display_tickets(ticket_dict)
            elif choice == 6:
                save_data(ticket_dict, ticket_counter)
                print("Data saved. Goodbye!")
                break
        except Exception as e:
            log.exception(f"Unexpected error in menu loop: {e}")

if __name__ == "__main__":
    main()