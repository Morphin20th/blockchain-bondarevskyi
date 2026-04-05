import sys

import uvicorn
from fastapi import FastAPI

from routes import router

app = FastAPI(title="Blockchain-API", debug=True)
app.include_router(router)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False)
