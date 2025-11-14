# Dockerfile for DA/PA Checker API
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables (optional, for production)
# ENV DB_ENGINE=mysql
# ENV DB_HOST=sql12.freesqldatabase.com
# ENV DB_PORT=3306
# ENV DB_USER=sql12807072
# ENV DB_PASSWORD=czWvibrE9c
# ENV DB_NAME=sql12807072

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
