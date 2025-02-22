FROM python:3.9-slim

WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Make the CLI script executable
RUN chmod +x cli.py

# Create an entrypoint that runs the CLI
ENTRYPOINT ["python", "cli.py"] 