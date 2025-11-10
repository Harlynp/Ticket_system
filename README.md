# IT Ticketing System
A lightweight, console-based **IT Ticketing System** with persistent storage, logging, and robust input validation.

## Features
- Create, update, reopen, and close tickets
- Persistent storage (`data/tickets.json`, `data/counter.txt`)
- Daily log files in `Log Files/YYYYMMDD.txt`
- Input validation with **3-attempt retry**
- **Close confirmation** to prevent accidental closure
- Stable sorting by creation date + ticket number
- Graceful error handling and I/O retry

## Folder Structure
project/
├── main.py              - Entry point
├── ticket.py            - Ticket logic and user flows
├── log.py               - Daily action logging
├── data/                - Auto-created: JSON + counter
│   ├── tickets.json
│   └── counter.txt
└── Log Files/           - Auto-created: daily logs
└── 20251110.txt

## Usage Guide

## Menu Options

Option     Action
1       Create Ticket – Enter description and technician username
2       Update Ticket – Modify open ticket
3       Reopen Ticket – Only closed tickets
4       Close Ticket – Final description + confirmation
5       View All Tickets – Sorted by date
6       Exit – Saves data automatically

## Input Rules

Field       Rules   
Description - 1–500 characters
Username - 1–50 chars, only letters, numbers, and dots (.)
Ticket Number - Auto-generated: AB1234 (first 2 letters of username + counter)

## Example Session

Welcome to IT Ticketing System

==================================================
1. Create Ticket
2. Update Ticket
3. Reopen Ticket
4. Close Ticket
5. View All Tickets
6. Exit
==================================================
Enter your choice (1-6): 1

Enter job description (max 500 chars): Printer not working in Room 101
Enter technician username (max 50 chars, alphanumeric or dots): john.doe

Success: Ticket JD1000 created.

Enter your choice (1-6): 5

------------------------------------------------------------------------------------------------------------------------
JD1000 - "Opened" - Printer not working in Room 101 - john.doe - 10/11/2025 - 10/11/2025
------------------------------------------------------------------------------------------------------------------------

## Persistence & Logs
Tickets are saved every time you create/update/reopen/close.
Counter persists to avoid duplicate ticket numbers.
Logs are appended daily in Log Files/YYYYMMDD.txt.

## Troubleshooting
Issue                                               Solution
data/ or Log Files/ not created     -       Run as user with write permissions
LOG-E01 error                       -       Check disk space or folder permissions
Tickets lost                        -       Check data/tickets.json for corruption


