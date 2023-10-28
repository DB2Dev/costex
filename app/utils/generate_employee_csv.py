import csv
from faker import Faker

fake = Faker()

with open("data/employees.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # header
    writer.writerow(["first_name", "middle_name", "last_name", "birth_date", "address"])
    for _ in range(1000000):
        writer.writerow([
            fake.first_name(),
            fake.last_name()[0], # Using last name first char as middle name
            fake.last_name(),
            fake.date(),
            fake.address().replace("\n", ", ")
        ])
