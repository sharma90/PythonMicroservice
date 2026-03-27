from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

# Equivalent to @ControllerAdvice

def register_exceptions(app):

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"message_GlobalExceptionHandler": str(exc)}
        )
    
    # this is to handle retry limit fallback, when rate limit exceeds then this function triggers
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return JSONResponse(
        status_code=429,
        content={"message": "Too many requests, try later"}  # fallback
    )