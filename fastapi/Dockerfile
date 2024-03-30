FROM python:3.9-slim-buster

# Move to the app directory
WORKDIR /app
ADD . /app

# Install requirements and export port
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

# Start the app
CMD sh -c 'uvicorn main:app --host 0.0.0.0 --port 80'