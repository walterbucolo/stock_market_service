# Stock_market_service
FastAPI app that authenticates a users and retrieve stock market information.

## API Documentation

View the Swagger documentation for the API [here](http://ec2-18-191-191-179.us-east-2.compute.amazonaws.com/docs).
> Note: A valid Api-key included in the headers is needed to retrieve stock information. 
> See in the documentation the POST users endpoints for more information on how to create an Api-key


## How to run it locally
1. Clone the repository.
2. Run ```cd stock_market_service``` to move to the app directory.
2. Run ```pip install -r requirements``` to install dependencies.
3. Run export ```VANTAGE_APIKEY=_your-vantange-apikey_``` to export vantage apikey.
4. Run ```uvicorn stock_market_app.main:app --reload``` to start the server.
5. Perform requests pointing to ```http://127.0.0.1:8000```


## How to run it using docker
1. Clone the repository.
2. Run ```cd stock_market_service``` to move to the app directory.
3. Make sure you have docker installed. Refer to https://docs.docker.com/engine/install/ to see how to install docker.
4. Run ```docker build -t stock_market .``` to build the image.
5. Run ```docker run -e API_KEY="<vantage-api-key>" -p 8000:8000 stock_market:latest``` to start the container
6. Perform requests pointing to ´http://0.0.0.0:8000/´

## How to access it in the cloud
1. Perform request to the following domain http://ec2-18-191-191-179.us-east-2.compute.amazonaws.com/
Example with curl: 
```
curl -X GET \
     -H "Content-Type: application/json" \
     -H "Api-key: <your-api-key>" \
     http://ec2-18-191-191-179.us-east-2.compute.amazonaws.com/api/stocks/meta
```

## Errata
There are somethins that are missing. I will try to add them in a PR

1. Integrations tests. 
2. API Throttling.
3. CI/CD for triggering automated tests per every PR and deploying to AWS
