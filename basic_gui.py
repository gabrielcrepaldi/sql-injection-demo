import customtkinter as ctk
import pyodbc
from tkinter import messagebox

# --- CONFIGURATION ---
# Ensure your SQL Server allows Windows Authentication for this string to work
CONN_STR = (
    'DRIVER={ODBC Driver 17 for SQL Server};' ##Search up your ODBC Drive and enter it here
    'SERVER=Newton\\SQLEXPRESS;' ##Search up your server name and enter it here
    'DATABASE=Factory;' 
    'Trusted_Connection=yes;'
)

# --- AUTHENTICATION LOGIC ---

def attempt_vulnerable_login():
    """Phase 1: Vulnerable to SQL Injection via ' OR '1'='1"""
    u = user_entry_vun.get()
    p = pw_entry_vun.get()
    
    # DANGEROUS: String formatting allows the user to break out of the quote marks
    query = f"SELECT * FROM Users WHERE Username = '{u}' AND Password = '{p}'"
    
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

        if row:
            # Transition to the SECURE login screen
            vun_frame.pack_forget()
            sec_frame.pack(pady=20, padx=20, fill="both", expand=True)
        else:
            messagebox.showerror("Error", "Invalid Credentials")
    except Exception as e:
        messagebox.showerror("Injection Error", f"SQL Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

def attempt_secure_login():
    """Phase 2: Protected using Parameterized Queries"""
    u = user_entry_sec.get()
    p = pw_entry_sec.get()
    
    # SECURE: '?' placeholders treat input as literal strings, not executable code
    query = "SELECT * FROM Users WHERE Username = ? AND Password = ?"
    
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        # Pass variables as a tuple to ensure sanitization
        cursor.execute(query, (u, p))
        row = cursor.fetchone()

        if row:
            sec_frame.pack_forget()
            main_frame.pack(fill="both", expand=True)
        else:
            messagebox.showerror("Error", "Access Denied: Secure Check Failed")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if 'conn' in locals(): conn.close()

# --- DATABASE LOGIC ---
def fetch_data():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Newton\\SQLEXPRESS;' 
        'DATABASE=Factory;'
        'Trusted_Connection=yes;' # For Windows Authentication
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    query = """
DECLARE @OutEID NVARCHAR(50), @OutName NVARCHAR(100), @OutDate NVARCHAR(50);
EXEC dbo.sp3 @OutEID OUTPUT, @OutName OUTPUT, @OutDate OUTPUT;
SELECT @OutEID, @OutName, @OutDate;
"""
    cursor.execute(query)
    
    result = cursor.fetchone()
    
    # Update the UI label with the data
    result_label.configure(text=str(result))
    conn.close()

# --- GUI FRAMEWORK ---
app = ctk.CTk()
app.geometry("500x400")
app.title("Security Progression Demo")

# --- FRAME 1: VULNERABLE LOGIN ---
vun_frame = ctk.CTkFrame(app)
vun_frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(vun_frame, text="PHASE 1: Vulnerable Login", font=("Arial", 20, "bold")).pack(pady=20)
ctk.CTkLabel(vun_frame, text="Try SQL Injection here", font=("Arial", 12), text_color="gray").pack()

user_entry_vun = ctk.CTkEntry(vun_frame, placeholder_text="Username")
user_entry_vun.pack(pady=10)

pw_entry_vun = ctk.CTkEntry(vun_frame, placeholder_text="Password") # Plain text for demo
pw_entry_vun.pack(pady=10)

ctk.CTkButton(vun_frame, text="Bypass Login", command=attempt_vulnerable_login).pack(pady=20)


# --- FRAME 2: SECURE LOGIN (Initially Hidden) ---
sec_frame = ctk.CTkFrame(app)

ctk.CTkLabel(sec_frame, text="PHASE 2: Secure Login", font=("Arial", 20, "bold"), text_color="#3a7ebf").pack(pady=20)
ctk.CTkLabel(sec_frame, text="Injection will not work here", font=("Arial", 12), text_color="gray").pack()

user_entry_sec = ctk.CTkEntry(sec_frame, placeholder_text="Username")
user_entry_sec.pack(pady=10)

pw_entry_sec = ctk.CTkEntry(sec_frame, placeholder_text="Password", show="*") # Hidden text
pw_entry_sec.pack(pady=10)

ctk.CTkButton(sec_frame, text="Secure Login", command=attempt_secure_login, fg_color="green", hover_color="darkgreen").pack(pady=20)


# --- FRAME 3: MAIN DASHBOARD (Initially Hidden) ---
main_frame = ctk.CTkFrame(app)

ctk.CTkLabel(main_frame, text="Database Dashboard", font=("Arial", 20, "bold")).pack(pady=20)
ctk.CTkButton(main_frame, text="Fetch Data", command=fetch_data).pack(pady=10)
result_label = ctk.CTkLabel(main_frame, text="Connection: Securely Authenticated", text_color="green")
result_label.pack(pady=10)

app.mainloop()
