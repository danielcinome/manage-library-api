import asyncio
import time

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
from starlette.status import (HTTP_503_SERVICE_UNAVAILABLE,
                              HTTP_504_GATEWAY_TIMEOUT)
from app.api.books import routers as books_router
from app.api.users import routers as users_router


app = FastAPI(title="Library management API")


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):

    # Time in seconds
    REQUEST_TIMEOUT_ERROR = 10

    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_ERROR)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse({'detail': 'Request processing time excedeed limit',
                             'processing_time': process_time},
                            status_code=HTTP_504_GATEWAY_TIMEOUT)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users_router.router,
    tags=["User"],
)

app.include_router(
    books_router.router,
    prefix="/books",
    tags=["Books"],
)