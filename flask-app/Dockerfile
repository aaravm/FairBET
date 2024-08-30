# Flask App Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN python3 -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=nillion-python-starter/quickstart/client_code/server.py
ENV PATH="/app/.venv/bin:$PATH"

# Run the Flask application when the container launches
CMD ["/bin/bash", "-c", "source .venv/bin/activate && flask run --host=0.0.0.0 --port=5000"]
