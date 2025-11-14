from fastapi import FastAPI
import logging
from app.api.routes import router
from app.db.database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Domain DA/PA Checker API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(router)
