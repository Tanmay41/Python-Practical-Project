import csv
import unittest

class Record:
    def __init__(self, id, name, age, department):
        self.id = id
        self.name = name
        self.age = age
        self.department = department

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Age: {self.age}, Department: {self.department}"

class Persistence:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self, file_path=None):
        if file_path is None:
            file_path = self.file_path
        records = []
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i >= 100:
                        break
                    records.append(Record(row['id'], row['name'], row['age'], row['department']))
            print("Data loaded successfully.")
        except FileNotFoundError:
            print("input.csv File not found, skipping data import.")
        return records
    def save_data(self, records):
        try:
            with open("output.csv", mode='w', newline='') as file:
                fieldnames = ['id', 'name', 'age', 'department']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([{'id': record.id, 'name': record.name, 'age': record.age, 'department': record.department} for record in records])
            print("Data saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving data: {e}")

class BusinessLogic:
    def __init__(self, records):
        self.records = records

    def display_records(self):
        for record in self.records:
            print(record)

    def add_record(self, id, name, age, department):
        new_record = Record(id, name, age, department)
        self.records.append(new_record)
        print("Record added successfully.")

    def update_record(self, id, new_name=None, new_age=None, new_department=None):
        for record in self.records:
            if record.id == id:
                record.name = new_name if new_name else record.name
                record.age = new_age if new_age else record.age
                record.department = new_department if new_department else record.department
                print("Record updated successfully.")
                return
        print("Record not found.")

    def delete_record(self, id):
        self.records = [record for record in self.records if record.id != id]
        print("Record deleted if it existed.")

# Presentation Layer (User Interaction)
def main():
    persistence = Persistence("input.csv")
    records = persistence.load_data()
    business_logic = BusinessLogic(records)

    while True:
        print("\n--- Menu ---")
        print("1. Display Records")
        print("2. Add Record")
        print("3. Update Record")
        print("4. Delete Record")
        print("5. Save Records")
        print("6. Reload Data")
        print("0. Exit")
        print("Program by [Your Name]")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            business_logic.display_records()
        elif choice == '2':
            id = input("Enter ID: ")
            name = input("Enter Name: ")
            age = input("Enter Age: ")
            department = input("Enter Department: ")
            business_logic.add_record(id, name, age, department)
        elif choice == '3':
            id = input("Enter ID to update: ")
            name = input("Enter New Name (leave blank to keep unchanged): ")
            age = input("Enter New Age (leave blank to keep unchanged): ")
            department = input("Enter New Department (leave blank to keep unchanged): ")
            business_logic.update_record(id, name if name else None, age if age else None, department if department else None)
        elif choice == '4':
            id = input("Enter ID to delete: ")
            business_logic.delete_record(id)
        elif choice == '5':
            persistence.save_data(business_logic.records)
        elif choice == '6':
            input_filename = input("Enter the filename to reload data from: ")
            records = persistence.load_data(input_filename)
            business_logic = BusinessLogic(records)
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

# Unit Testing
class TestBusinessLogic(unittest.TestCase):
    def setUp(self):
        self.records = [Record('1', 'Alice', 25, 'HR')]
        self.logic = BusinessLogic(self.records)

    def test_add_record(self):
        self.logic.add_record('2', 'Bob', 30, 'IT')
        self.assertEqual(len(self.records), 2)

    def test_update_record(self):
        self.logic.update_record('1', new_name='Alice Cooper')
        self.assertEqual(self.records[0].name, 'Alice Cooper')

    def test_delete_record(self):
        self.logic.delete_record('1')
        self.assertEqual(len(self.records), 0)


main()  # Start the main program loop
# Run unit tests if desired (uncomment the line below)
# unittest.main()
