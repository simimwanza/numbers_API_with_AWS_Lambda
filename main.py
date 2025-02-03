from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import requests
import math
from fastapi.responses import JSONResponse

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
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == abs(n)

def is_armstrong(n: int) -> bool:
    num_str = str(abs(n))
    num_digits = len(num_str)
    return sum(int(d) ** num_digits for d in num_str) == abs(n)

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

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
        fact = response.text
        return fact.replace("\n", "").strip()
    except:
        return f"{n} is a number"

@app.get("/api/classify-number")
async def classify_number(number: str):
    # Input validation
    if not number:
        return JSONResponse(
            status_code=400,
            content={"number": None, "error": True}
        )
    
    try:
        # Convert to float first to handle decimal points
        num_float = float(number)
        # Convert to integer (truncating any decimal part)
        num = int(num_float)
        
        response_data = {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": get_properties(num),
            "digit_sum": get_digit_sum(num),
            "fun_fact": get_fun_fact(num)
        }
        return JSONResponse(
            status_code=200,
            content=response_data
        )
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"number": number, "error": True}
        )

# Handler for AWS Lambda
handler = Mangum(app)
