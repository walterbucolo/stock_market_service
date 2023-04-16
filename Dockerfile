# Define the base image
FROM python:3.11.2

# Copy the app files to the Docker image
COPY . /app

# Set the working directory to the app directory
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port that the app is listening on
EXPOSE 8000

# Start the app 
CMD ["uvicorn", "stock_market_app.main:app", "--host", "0.0.0.0", "--port", "8000"]