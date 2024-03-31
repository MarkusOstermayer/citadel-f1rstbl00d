FROM python:3.11-slim

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

WORKDIR /app
COPY . /app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

# Copy supervisord configuration file
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /fastapi

# Run supervisord
CMD ["/usr/bin/supervisord"]