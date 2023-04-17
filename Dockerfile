FROM python:3.11.2

COPY . /app

WORKDIR /app

ENV VANTAGE_API_KEY = "API-KEY"

RUN pip install -r requirements.txt

EXPOSE 8000

# Start the app 
CMD ["uvicorn", "stock_market_app.main:app", "--host", "0.0.0.0", "--port", "8000"]