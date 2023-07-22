from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Exception handler for RequestValidationError (input validation errors)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation Error", "errors": exc.errors()},
    )

# Exception handler for IntegrityError (database integrity errors)
async def integrity_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Database Integrity Error"},
    )

# Exception handler for generic HTTPException (other HTTP errors)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Exception handler for generic Python exceptions (server errors)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )