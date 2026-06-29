from fastapi import FastAPI, Query, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid

app = FastAPI()

EMAIL = "23f2000729@ds.study.iitm.ac.in"

ALLOWED_ORIGIN = "https://dash-4t0zvc.example.com"

# Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# Middleware for headers
@app.middleware("http")
async def add_headers(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{duration:.6f}"

    return response


# Preflight support
@app.options("/stats")
async def options_stats():
    return Response(status_code=200)


@app.get("/stats")
async def stats(values: str = Query(...)):

    nums = [int(x.strip()) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 2)
    }