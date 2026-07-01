from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.routers import auth, predict, report
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SteelSight API",
    version="1.0.0",
)

@app.middleware("http")
async def cors_handler(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Max-Age"]       = "86400"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(report.router)

@app.get("/")
def root():
    return {"status": "SteelSight API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}