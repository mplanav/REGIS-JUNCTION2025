#Base image with python 3.11
FROM python:3.11-slim

#Set working directory
WORKDIR /app

#Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

#Copy requirements file
COPY requirements.txt /app/requirements.txt 

#Install python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

#Copy application code
COPY . /app

#Expose FASTAPI port
EXPOSE 8000

#Command to run Fastapi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]