import sqlite3
import unittest

# Record Class for Data Representation
class Record:
    def __init__(self, id, name, age, department):
        self.id = id
        self.name = name
        self.age = age
        self.department = department

    def display(self, format_type="regular"):
        if format_type == "detailed":
            return f"[Detailed View]\nID: {self.id}\nName: {self.name}\nAge: {self.age}\nDepartment: {self.department}\n"
        elif format_type == "simple":
            return f"{self.id} - {self.name}"
        else:  # Regular display
            return f"ID: {self.id}, Name: {self.name}, Age: {self.age}, Department: {self.department}"

# Database Layer (SQLite Integration)
class Database:
    def __init__(self, db_name="records.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                                id TEXT PRIMARY KEY,
                                name TEXT,
                                age INTEGER,
                                department TEXT)''')
        self.connection.commit()

    def load_data(self):
        records = []
        self.cursor.execute("SELECT * FROM records")
        rows = self.cursor.fetchall()
        for row in rows:
            records.append(Record(*row))
        print(f"{len(records)} records loaded from the database.")
        return records

    def save_record(self, record):
        self.cursor.execute('''INSERT OR REPLACE INTO records (id, name, age, department)
                               VALUES (?, ?, ?, ?)''', (record.id, record.name, record.age, record.department))
        self.connection.commit()

    def delete_record(self, record_id):
        self.cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()

# Business Logic Layer (CRUD Operations)
class BusinessLogic:
    def __init__(self, db):
        self.db = db
        self.records = self.db.load_data()

    def display_records(self, format_type="regular"):
        for record in self.records:
            print(record.display(format_type))

    def add_record(self, id, name, age, department):
        new_record = Record(id, name, age, department)
        self.records.append(new_record)
        self.db.save_record(new_record)
        print("Record added successfully.")

    def update_record(self, id, new_name=None, new_age=None, new_department=None):
        for record in self.records:
            if record.id == id:
                record.name = new_name if new_name else record.name
                record.age = new_age if new_age else record.age
                record.department = new_department if new_department else record.department
                self.db.save_record(record)
                print("Record updated successfully.")
                return
        print("Record not found.")

    def delete_record(self, id):
        self.records = [record for record in self.records if record.id != id]
        self.db.delete_record(id)
        print("Record deleted if it existed.")

# Presentation Layer (User Interaction)
def main():
    db = Database()
    business_logic = BusinessLogic(db)

    while True:
        print("\n--- Menu ---")
        print("1. Display Records (Regular View)")
        print("2. Display Records (Detailed View)")
        print("3. Display Records (Simple View)")
        print("4. Add Record")
        print("5. Update Record")
        print("6. Delete Record")
        print("0. Exit")
        print("Program by [Your Name]")

        choice = input("Enter your choice: ")
        if choice == '1':
            business_logic.display_records(format_type="regular")
        elif choice == '2':
            business_logic.display_records(format_type="detailed")
        elif choice == '3':
            business_logic.display_records(format_type="simple")
        elif choice == '4':
            id = input("Enter ID: ")
            name = input("Enter Name: ")
            age = input("Enter Age: ")
            department = input("Enter Department: ")
            business_logic.add_record(id, name, age, department)
        elif choice == '5':
            id = input("Enter ID to update: ")
            name = input("Enter New Name (leave blank to keep unchanged): ")
            age = input("Enter New Age (leave blank to keep unchanged): ")
            department = input("Enter New Department (leave blank to keep unchanged): ")
            business_logic.update_record(id, name if name else None, age if age else None, department if department else None)
        elif choice == '6':
            id = input("Enter ID to delete: ")
            business_logic.delete_record(id)
        elif choice == '0':
            db.close()
            break
        else:
            print("Invalid choice. Please try again.")

# Unit Testing for Display Formats
class TestDisplayFormats(unittest.TestCase):
    def setUp(self):
        self.record = Record('1', 'Alice', 25, 'HR')

    def test_regular_display(self):
        self.assertEqual(self.record.display(), "ID: 1, Name: Alice, Age: 25, Department: HR")

    def test_detailed_display(self):
        self.assertIn("[Detailed View]", self.record.display(format_type="detailed"))

    def test_simple_display(self):
        self.assertEqual(self.record.display(format_type="simple"), "1 - Alice")

if __name__ == "__main__":
    main()

    # Uncomment the next line to run the unit tests
    # unittest.main()
