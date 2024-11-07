import csv

class Record:
    def __init__(self, name, age, salary):
        """
        Parameters:
        name (str).
        age (int).
        salary (float).
        """
        self.name = name
        self.age = age
        self.salary = salary

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Salary: {self.salary}"

def read_data_from_file(file_path):
    """
    Parameters:
    file_path (str).
    """
    records = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            
            for row in csv_reader:
                name, age, salary = row[0], int(row[1]), float(row[2])
                record = Record(name, age, salary)
                records.append(record)

    except FileNotFoundError:
        print("Error: The file was not found.")
    except ValueError as e:
        print(f"Data formatting error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return records

def display_records(records):
    """
    Parameters:
    records (list)
    """
    print("Displaying all records:")
    for record in records:
        print(record)


sample_record = [Record("Alice", 30, 75000.0), Record("Bob", 25, 50000.0), Record("Charlie", 28, 60000.0)]

display_records(sample_record)

new_sample_record = read_data_from_file("./file.csv")

display_records(new_sample_record)