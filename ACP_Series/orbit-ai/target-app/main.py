from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import random

app = FastAPI()

# Total request counter
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total App HTTP Requests"
)

# Request latency tracker
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency"
)

# REQUEST_COUNT (Counter): Keeps track of the total number of HTTP requests received by the application across all endpoints.
# REQUEST_LATENCY (Histogram): Measures and tracks the distribution of request latencies (durations) in seconds.


@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {"message": "OrbitAI Target App Running"}


@app.get("/health")
def health():
    REQUEST_COUNT.inc()
    return {"status": "healthy"}


@app.get("/slow-api")
def slow_api():
    REQUEST_COUNT.inc()

    start_time = time.time()

    # Simulate slow API
    sleep_time = random.randint(2, 5)
    time.sleep(sleep_time)

    REQUEST_LATENCY.observe(time.time() - start_time)

    return {
        "message": "Slow API response",
        "delay": sleep_time
    }


@app.get("/random-error")
def random_error():
    REQUEST_COUNT.inc()

    if random.random() > 0.5:
        return {"status": "success"}

    return Response(
    )