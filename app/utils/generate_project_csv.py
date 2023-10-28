import csv
from faker import Faker

fake = Faker()

with open("data/projects.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # header
    writer.writerow(["project_name", "project_desc", "mgr_ssn"])
    for _ in range(1000000):
        writer.writerow([
            fake.company(),
            fake.catch_phrase(),
            "EM"+str(100001+_)
        ])
