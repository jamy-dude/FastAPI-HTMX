from loguru import logger
from app.app import app  # Add this line

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn in reload mode")
    uvicorn.run(
        app,  # Change this line
        host="127.0.0.1",
        reload=True,
        port=8080,
    )