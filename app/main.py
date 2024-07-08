
from logging_config import logger
from fastapi import FastAPI
import models
from app.database import engine
from app.routers import healthcheck , contacts

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
app.include_router(healthcheck.router, tags=["healthcheck"])

# Root endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint was called")
    return {"message": "Welcome to the contact API"}

logger.info("Application setup complete")