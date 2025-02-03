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
