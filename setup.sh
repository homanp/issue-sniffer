#!/bin/bash

# Create and activate the virtual environment
virtualenv venv
source venv/bin/activate

# Read the variable names from the `env.example` file
for var in $(cat .env.example); do
  # Ask the user for input
  echo "Please provide the value for $var:"
  read -r value

  # Save the value to the `.env` file
  echo "$var$value" >> .env
done

# Install dependencies using Poetry
poetry install

# Run Prisma migration
poetry run prisma migrate dev

# Start the application with auto-reload
uvicorn app.main:app --reload
