FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the Flask app
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Default command to run the app using Flask's built‑in server
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]