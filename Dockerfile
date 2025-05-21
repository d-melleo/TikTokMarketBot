# Use an official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy only requirement files to install dependencies first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Run the bot
CMD ["python", "main.py"]