import sqlite3
from tabulate import tabulate


def setup_address_book():
    # 1. Connect to an in-memory SQLite database (or change to 'address_book.db' to save to a file)
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    print("Step 1: Creating the 'contacts' table...")
    # 2. Create the main table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            city TEXT,
            category TEXT -- e.g., Family, Work, Friend
        )
    """
    )

    print("Step 2: Inserting sample data...")
    # 3. Insert some sample data
    sample_contacts = [
        (
            "Alice",
            "Smith",
            "555-0123",
            "alice.smith@email.com",
            "New York",
            "Work",
        ),
        (
            "Bob",
            "Jones",
            "555-4567",
            "bob.j@email.com",
            "San Francisco",
            "Family",
        ),
        (
            "Charlie",
            "Brown",
            "555-8910",
            "charlie.b@email.com",
            "Chicago",
            "Friend",
        ),
        (
            "Diana",
            "Prince",
            "555-1111",
            "diana@email.com",
            "New York",
            "Work",
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO contacts (first_name, last_name, phone, email, city, category)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        sample_contacts,
    )

    print("Step 3: Creating a SQL View (v_work_contacts)...")
    # 4. Create a SQL View (combining names and filtering only 'Work' contacts)
    cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS v_work_contacts AS
        SELECT 
            first_name || ' ' || last_name AS full_name,
            phone,
            email,
            city
        FROM contacts
        WHERE category = 'Work'
    """
    )

    conn.commit()
    return conn


def view_results(conn):
    print("\n--- Displaying Data via SQL View ---")
    cursor = conn.cursor()

    # 5. Query the SQL View just like a normal table
    cursor.execute("SELECT * FROM v_work_contacts")
    rows = cursor.fetchall()

    # Get column headers from the view description
    headers = [description[0] for description in cursor.description]

    # 6. Print the results in a well-formatted table
    print(tabulate(rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    # Run the setup and display the view
    db_connection = setup_address_book()
    view_results(db_connection)

    # Clean up
    db_connection.close()

