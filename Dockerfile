# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_APP=app

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Define a health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["flask", "run"]
