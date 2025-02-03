from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import requests
import math

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    num_str = str(n)
    num_digits = len(num_str)
    return sum(int(d) ** num_digits for d in num_str) == n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

def get_properties(n: int) -> list:
    properties = []
    if is_armstrong(n):
        properties.append("armstrong")
    if n % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math")
        return response.text
    except:
        return f"{n} is a number"

@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        num = int(number)
    except ValueError:
        return {"number": number, "error": True}

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": get_properties(num),
        "digit_sum": get_digit_sum(num),
        "fun_fact": get_fun_fact(num)
    }

# Handler for AWS Lambda
handler = Mangum(app)
