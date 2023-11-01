#!/bin/bash

cd "$(dirname "$0")"

cd ..

cd ..

# Run the Python scripts to generate data then copy them to the DB
python3 -m app.data.generate_employees
python3 -m app.data.generate_projects
python3 -m app.utils.seed

echo "Data generation and seeding done!"
