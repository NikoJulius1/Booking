# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Run the database initialization script
RUN python reservationdatabase.py

# Expose the port Gunicorn runs on
EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]