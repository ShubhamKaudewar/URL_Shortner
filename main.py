from fastapi import FastAPI

from src.routers import limiter, router as url_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

app.include_router(url_router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
def read_root():
    return "Server is running."


# if __name__ == "__main__":
#     input_url = "https://www.geeksforgeeks.org/system-design-interview-bootcamp"
#     result = main(input_url)
#     print(result)
