FROM python:3.12

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your application files into /app
COPY app/ .
RUN ls -l /app # Debugging line to list files in /app

# Default command (optional, can be overridden in docker-compose)
CMD ["python", "main_getter.py"]

