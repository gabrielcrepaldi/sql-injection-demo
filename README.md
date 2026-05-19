# SQL Injection Vulnerability Demo

A Python desktop application that demonstrates a SQL injection attack and its remediation side by side. Built as part of the Advanced Database Systems course at the University of South Florida.

---

## What This Project Demonstrates

SQL injection is one of the most common and dangerous web vulnerabilities — ranked in the [OWASP Top 10](https://owasp.org/www-project-top-ten/) for decades. This application walks through the attack and the fix in a hands-on, visual way using a real SQL Server database backend.

The app progresses through three phases:

| Phase | Description |
|-------|-------------|
| **Phase 1 — Vulnerable Login** | A login form built with unsafe string formatting. Open to SQL injection bypass. |
| **Phase 2 — Secure Login** | The same form rebuilt using parameterized queries. Injection attempts are neutralized. |
| **Phase 3 — Dashboard** | Authenticated access to a database dashboard that executes stored procedures. |

---

## The Attack — Phase 1

The vulnerable query is constructed by directly embedding user input into a SQL string:

```python
query = f"SELECT * FROM Users WHERE Username = '{u}' AND Password = '{p}'"
```

An attacker can bypass authentication entirely by entering the following in either field:

```
Username: ' OR '1'='1
Password: ' OR '1'='1
```

This transforms the query into:

```sql
SELECT * FROM Users WHERE Username = '' OR '1'='1' AND Password = '' OR '1'='1'
```

Since `'1'='1'` is always true, the `WHERE` clause evaluates to `TRUE` for every row — granting access without valid credentials.

---

## The Fix — Phase 2

The secure version replaces string formatting with **parameterized queries** using `?` placeholders:

```python
query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
cursor.execute(query, (u, p))
```

The database driver treats the user input as **literal data**, never as executable SQL. The same injection string is interpreted as a username to look up — not as logic to execute — and authentication is correctly denied.

---

## Tech Stack

- **Python 3.x**
- **CustomTkinter** — modern GUI framework
- **pyodbc** — SQL Server connectivity
- **SQL Server Express** — database backend (Windows Authentication)

---

## Setup & Requirements

### Prerequisites

```bash
pip install customtkinter pyodbc
```

You will also need:
- SQL Server Express (or full SQL Server) installed locally
- ODBC Driver 17 for SQL Server
- A database named `Factory` with a `Users` table containing `Username` and `Password` columns
- A stored procedure `dbo.sp3` returning employee data (for the dashboard phase)

### Configuration

Open `basic_gui.py` and update the connection string to match your environment:

```python
CONN_STR = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=YourServerName\\SQLEXPRESS;'
    'DATABASE=Factory;'
    'Trusted_Connection=yes;'
)
```


## Author

**Gabriel Garcia Crepaldi**  
B.S. Cybersecurity — University of South Florida, 2026  
[LinkedIn](https://www.linkedin.com/in/gabriel-crepaldi-ab7b18388/) · [GitHub](https://github.com/gabrielcrepaldi)
