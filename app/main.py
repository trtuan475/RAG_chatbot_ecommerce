from fastapi import FastAPI
import logging 

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title = "RAG Chatbot",
    version = "1.0"
)

@app.get("/")
def test():
    return {
        "status": "online",
        "message": "Welcome"
    }

logger.info("Run server FastAPI")