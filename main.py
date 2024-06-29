import os

import uvicorn

from src.config.config import ENVIRON

if __name__ == "__main__":
    if ENVIRON == 'dev':
        uvicorn.run("src.app:app", host="127.0.0.1", port=8001, reload=True)
    elif ENVIRON == 'prd' or ENVIRON == 'prod':
        uvicorn.run("src.app:app", host="0.0.0.0", port=80, reload=True)
