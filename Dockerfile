# Using python 3.11 slim image for project.
FROM python:3.11-slim

# Set the working directory. 
WORKDIR /app

# Copy all requirements and install them.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app.py Code.
COPY app.py .

# Expose Port 5000 for Local Host.
EXPOSE 5000

# Start the Application.
CMD ["python", "app.py"]