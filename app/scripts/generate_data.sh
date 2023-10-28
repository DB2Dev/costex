#!/bin/bash

cd "$(dirname "$0")"

cd ..

# Run the Python scripts to generate data
python3 ./utils/generate_employee_csv.py
python3 ./utils/generate_project_csv.py

echo "Data generation complete!"
