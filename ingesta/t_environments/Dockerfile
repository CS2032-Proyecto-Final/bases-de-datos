FROM python:3.9-slim

# Install necessary libraries
RUN pip3 install --no-cache-dir boto3 loguru

# Create the AWS configuration directory
RUN mkdir -p ~/.aws

RUN mkdir -p ~/.aws-eduardo

# Set the working directory
WORKDIR /usr/src/app

# Copy the source code into the container
COPY . .

# Use the listener script as the entry point
CMD ["bash", "-c", "python3 ./pull_environments.py && python3 ./load_environments.py"]
