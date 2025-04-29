import csv
import os
from datetime import datetime
from tabulate import tabulate

def create_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Description', 'Amount'])

def append_entry(file_path, date, description, amount):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])

def read_entries(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def print_entries(file_path):
    data = read_entries(file_path)
    print(tabulate(data[1:], headers=data[0], tablefmt='pretty'))

def report_sum(file_path, year=None, month=None):
    data = read_entries(file_path)[1:]
    total = 0.0
    for row in data:
        try:
            date_obj = datetime.strptime(row[0], '%Y-%m-%d')
            amount = float(row[2])
            if year and date_obj.year != int(year):
                continue
            if month and date_obj.month != int(month):
                continue
            total += amount
        except (ValueError, IndexError):
            continue
    print(f"Total amount for year={year} month={month}: {total:.2f}")

if __name__ == "__main__":
    FILE_PATH = 'transactions.csv'
    create_csv(FILE_PATH)

    while True:
        print("\nOptions:")
        print("1. Add entry")
        print("2. View all entries")
        print("3. Report total (filter by year/month)")
        print("4. Exit")
        choice = input("Select option: ")

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            description = input("Enter description: ")
            amount = input("Enter amount: ")
            append_entry(FILE_PATH, date, description, amount)
        elif choice == '2':
            print_entries(FILE_PATH)
        elif choice == '3':
            year = input("Enter year (or press Enter to skip): ")
            month = input("Enter month (1-12) (or press Enter to skip): ")
            year = year if year else None
            month = month if month else None
            report_sum(FILE_PATH, year, month)
        elif choice == '4':
            break
        else:
            print("Invalid option.")
