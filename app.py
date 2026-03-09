import uvicorn
from fastapi import FastAPI
from routes import router

app = FastAPI(title="Blockchain-API", debug=True)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
