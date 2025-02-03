### Resources
- Fun fact API: http://numbersapi.com/#42
- https://en.wikipedia.org/wiki/Parity_(mathematics)

# Task Description: DevOps Stage 1 - Number Classification API

Create an API that takes a number and returns interesting mathematical properties about it, along with a fun fact.
Weight: 6 points
Requirements

    Technology Stack:
        Use any programming language or framework of your choice (See Sharp (C #), PHP :elephant:, Python :snake:, Go :runner::skin-tone-5:, Java :coffee:, JS/TS :nauseated_face:)
        Must be deployed to a publicly accessible endpoint
        Must handle CORS (Cross-Origin Resource Sharing)
        Must return responses in JSON format
    Version Control:
        Code must be hosted on GitHub
        Repository must be public
        Must include a well-structured README.md

API Specification

    Endpoint: **GET** <your-url>/api/classify-number?number=371
    Required JSON Response Format (200 OK):

```
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,  // sum of its digits
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
}

    Required JSON Response Format (400 Bad Request)

{
    "number": "alphabet",
    "error": true
}
```



Deployment

    Publicly accessible and stable API.
    Fast response time (< 500ms).

Additional Note

    Use the math type from the Numbers API to get the fun fact.
    The possible combinations for the properties field:
        ["armstrong", "odd"] - if the number is both an Armstrong number and odd
        ["armstrong", “even”] - if the number is an Armstrong number and even
        ["odd"] - if the number is not an Armstrong number but is odd
        [”even”] - if the number is not an Armstrong number but is even


## How to deploy the API to AWS

#### Create and activate virtual environment
```
python -m venv venv
source venv/bin/activate 
```

### Install dependencies
```
pip install -r requirements.txt
```

### Create package directory
```
mkdir package
```

### Install dependencies in package directory
```
pip install --target ./package -r requirements.txt
```

### Copy lambda function to package
```
cp main.py package/
```

### Create deployment ZIP
```
cd package
zip -r ../deployment.zip .
cd ..
```

## Using AWS CLI

### Create Lambda function
```
aws lambda create-function \
    --function-name number-classifier \
    --runtime python3.9 \
    --handler lambda_function.handler \
    --role arn:aws:iam::[YOUR-ACCOUNT-ID]:role/[YOUR-LAMBDA-ROLE] \
    --zip-file fileb://deployment.zip \
    --timeout 30 \
    --memory-size 256
```

### For updates, use:

```
aws lambda update-function-code \
    --function-name number-classifier \
    --zip-file fileb://deployment.zip

    Set up API Gateway:
```

### Create API

```
aws apigateway create-rest-api \
    --name "Number-Classifier-API" \
    --description "Number Classification API"
```

### Get API ID
```
API_ID=$(aws apigateway get-rest-apis --query "items[?name=='Number-Classifier-API'].id" --output text)
```

### Get root resource ID
```
ROOT_RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/'].id" --output text)
```
### Create resource
```
aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_RESOURCE_ID \
    --path-part "api"
```

### Create method
```
aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method GET \
    --authorization-type NONE
```

### Create integration
```
aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $RESOURCE_ID \
    --http-method GET \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:${AWS_REGION}:lambda:path/2015-03-31/functions/${LAMBDA_ARN}/invocations
```
## Deploy the API:

### Create deployment
```
aws apigateway create-deployment \
    --rest-api-id $API_ID \
    --stage-name prod
``` 

