# Use official Python image as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install the Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your FastAPI app into the container
COPY . .

# Expose the port that Uvicorn will run on (default FastAPI port)
EXPOSE 8000

# Command to run the Uvicorn server on a specified address
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
