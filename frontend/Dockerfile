# Base image with Python 3.10
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirement dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend application files
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Run Streamlit with headlessly enabled and listening on all interfaces
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
