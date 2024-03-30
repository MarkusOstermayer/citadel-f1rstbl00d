FROM python:3.9-slim-buster

# Move to the app directory
WORKDIR /app
COPY . /app

# Install requirements 
RUN pip install --no-cache-dir -r requirements.txt

# Start the app
CMD ["python", "main.py"]