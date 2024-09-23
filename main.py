from fastapi import FastAPI
from translator.routes import router as translator_router

app = FastAPI(
    title="audio_api",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
)

app.include_router(router=translator_router, prefix="/translator", tags=["translator"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")
