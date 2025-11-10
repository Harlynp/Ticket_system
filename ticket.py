# ticket.py
"""
Core ticket domain logic with full OOP encapsulation.
"""
from __future__ import annotations
from datetime import datetime
import re
from typing import Dict, Optional
from log import log_action
from config import (
    MAX_DESCRIPTION_LENGTH, MAX_USERNAME_LENGTH, USERNAME_REGEX,
    DATE_FORMAT, DEFAULT_COUNTER
)

class Ticket:
    def __init__(self, ticket_number: str, username: str, description: str):
        self.ticket_number = ticket_number
        self.username = username
        self.description = description
        self.status = "Opened"
        now = datetime.now().strftime(DATE_FORMAT)
        self.created_date = now
        self.updated_date = now

    def update(self, description: str) -> None:
        self.description = description
        self.status = "Updated"
        self.updated_date = datetime.now().strftime(DATE_FORMAT)
        log_action("UPDATE", self)

    def reopen(self, description: str) -> None:
        self.description = description
        self.status = "Reopened"
        self.updated_date = datetime.now().strftime(DATE_FORMAT)
        log_action("REOPEN", self)

    def close(self, final_desc: str) -> None:
        self.description = final_desc
        self.status = "Closed"
        self.updated_date = datetime.now().strftime(DATE_FORMAT)
        log_action("CLOSE", self)

    def __str__(self) -> str:
        return (f"{self.ticket_number} - \"{self.status}\" - {self.description} - "
                f"{self.username} - {self.created_date} - {self.updated_date}")

    def __repr__(self) -> str:
        return f"Ticket({self.ticket_number!r}, {self.username!r})"

# === Input Retry Helper ===
def retry_input(prompt: str, validator, error_msg: str, max_attempts: int = 3) -> Optional[str]:
    for attempt in range(max_attempts):
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"{error_msg} ({max_attempts - attempt - 1} attempts left)")
    print("Too many invalid attempts. Operation cancelled.")
    return None

# === Validators ===
def validate_description(d: str) -> bool:
    return bool(d) and len(d) <= MAX_DESCRIPTION_LENGTH

def validate_username(u: str) -> bool:
    """Ensure username is safe and within limits.
    - Alphanumeric + dots only (prevents injection/path issues)
    - Max 50 chars (UI and storage limits)
    """
    return (bool(u) and len(u) <= MAX_USERNAME_LENGTH and
            re.match(USERNAME_REGEX, u) is not None)

# === Ticket Operations (Orchestration) ===
def create_ticket(ticket_dict: Dict[str, Ticket], counter: int) -> bool:
    desc = retry_input(
        f"Enter job description (max {MAX_DESCRIPTION_LENGTH} chars): ",
        validate_description,
        "Description must be non-empty and ≤500 characters."
    )
    if not desc:
        return False

    username = retry_input(
        f"Enter technician username (max {MAX_USERNAME_LENGTH} chars): ",
        validate_username,
        "Username must be non-empty, ≤50 chars, alphanumeric or dots."
    )
    if not username:
        return False

    prefix = (username[:2].upper() if len(username) >= 2 else (username + "X")[:2].upper())
    ticket_number = f"{prefix}{counter}"
    ticket = Ticket(ticket_number, username, desc)
    ticket_dict[ticket_number] = ticket
    log_action("CREATE", ticket)
    print(f"Success: Ticket {ticket_number} created.")
    return True

def update_ticket(ticket_dict: Dict[str, Ticket]) -> None:
    ticket_number = retry_input(
        "Enter ticket number to update: ",
        lambda x: x in ticket_dict,
        "Ticket not found."
    )
    if not ticket_number:
        return
    ticket = ticket_dict[ticket_number]
    if ticket.status == "Closed":
        print("Error: Cannot update closed ticket.")
        return

    new_desc = retry_input(
        f"Enter new description (max {MAX_DESCRIPTION_LENGTH} chars): ",
        validate_description,
        "Description must be non-empty and ≤500 characters."
    )
    if new_desc:
        ticket.update(new_desc)
        print(f"Success: Ticket {ticket_number} updated.")

def reopen_ticket(ticket_dict: Dict[str, Ticket]) -> None:
    ticket_number = retry_input(
        "Enter ticket number to reopen: ",
        lambda x: x in ticket_dict and ticket_dict[x].status == "Closed",
        "Only closed tickets can be reopened."
    )
    if not ticket_number:
        return
    ticket = ticket_dict[ticket_number]

    new_desc = retry_input(
        f"Enter updated description (max {MAX_DESCRIPTION_LENGTH} chars): ",
        validate_description,
        "Description must be non-empty and ≤500 characters."
    )
    if new_desc:
        ticket.reopen(new_desc)
        print(f"Success: Ticket {ticket_number} reopened.")

def close_ticket(ticket_dict: Dict[str, Ticket]) -> None:
    ticket_number = retry_input(
        "Enter ticket number to close (or blank to cancel): ",
        lambda x: not x or (x in ticket_dict and ticket_dict[x].status != "Closed"),
        "Ticket not found or already closed."
    )
    if not ticket_number:
        return
    ticket = ticket_dict[ticket_number]

    confirm = input(f"Close ticket {ticket_number}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Close cancelled.")
        return

    final_desc = retry_input(
        f"Enter final description (max {MAX_DESCRIPTION_LENGTH} chars): ",
        validate_description,
        "Description must be non-empty and ≤500 characters."
    )
    if final_desc:
        ticket.close(final_desc)
        print(f"Success: Ticket {ticket_number} closed.")