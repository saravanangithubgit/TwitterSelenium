# Use the official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome stable version
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && apt-get clean && rm -rf /var/lib/apt/lists/*


# Create and set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
