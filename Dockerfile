# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye

# Install dependencies and Microsoft ODBC driver
RUN apt-get update && \
    apt-get install -y curl gnupg2 apt-transport-https unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --allow-downgrades msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set workdir and copy files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000


# Start your app using Gunicorn (recommended for production)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]