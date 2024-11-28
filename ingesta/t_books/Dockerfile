FROM python:3.9-slim

# Install necessary libraries
RUN pip3 install --no-cache-dir boto3

# Create the AWS configuration directory
RUN mkdir -p ~/.aws

# Set the working directory
WORKDIR /usr/src/app

# Copy the source code into the container
COPY . .

# Use the listener script as the entry point
CMD ["python3", "./pull_books.py"]

CMD ["python3", "./load_books.py"]