from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse

# Import your QA pipeline class
from app.qa_pipeline import QAPipeline

app = FastAPI()

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# Handle rate limit exceeded errors
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )

# Initialize your QA pipeline (adjust constructor as needed)
pipeline = QAPipeline()

# Rate-limited endpoint, remember to include 'request' param
@app.post("/ask")
@limiter.limit("5/minute")
async def ask(request: Request, question: str):
    # Call your QA pipeline to get answer
    answer = pipeline.get_answer(question)  # Adjust method name to your implementation
    return {"answer": answer}
