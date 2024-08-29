# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /home/nillion-python-starter

# Install curl
RUN apt-get update && apt-get install -y curl

# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /home/nillion-python-starter

# Install curl and bash
RUN apt-get update && apt-get install -y curl bash

# Download and install nilup and nillion
RUN curl https://nilup.nilogy.xyz/install.sh | bash \
    && bash -c "source /root/.bashrc && nilup install latest && nilup use latest && nilup init"

# Verify Python and pip installation
RUN python3 --version \
    && python3 -m pip --version

# Set up a virtual environment
RUN python3 -m venv .venv

# Verify Python and pip installation
RUN python3 --version \
    && python3 -m pip --version

# Set up a virtual environment
RUN python3 -m venv .venv

# Copy the requirements.txt file into the container
COPY nillion-python-starter/requirements.txt .

# Activate the virtual environment and install dependencies
RUN /bin/bash -c "source .venv/bin/activate && pip install --upgrade -r requirements.txt"

# Make sure nillion-devnet is available in PATH
RUN ln -s /root/.nilup/bin/nillion-devnet /usr/local/bin/nillion-devnet

# Run nillion-devnet when the container launches
CMD ["/bin/bash", "-c", "source .venv/bin/activate && nillion-devnet"]
