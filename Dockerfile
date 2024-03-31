FROM python:3.11-slim-bookworm

# Install supervisord
RUN apt-get update && apt-get install -y supervisor

# Set workdir
WORKDIR /app

# Copy and Install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files and supervisord configuration file
COPY ./webdc webdc
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# expose port 80
EXPOSE 80

# Run supervisord
CMD ["/usr/bin/supervisord"]
