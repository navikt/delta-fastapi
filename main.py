from fastapi import FastAPI
from app.routers import include_routers
from app.config import configure_cors, configure_database, configure_exceptions, configure_openapi

app = FastAPI()

# Routere legges til i /app/routers/__init__.py
include_routers(app)

# Konfig
configure_cors(app)
configure_database(app)
configure_exceptions(app)
configure_openapi(app)

if __name__ == "__main__":
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=8087
    )
