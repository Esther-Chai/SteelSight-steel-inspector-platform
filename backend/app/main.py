from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.routers import auth, predict, report
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SteelSight API", version="1.0.0")

# Manual CORS middleware to handle preflight
@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
        response.headers["Access-Control-Allow-Origin"]  = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Max-Age"]       = "3600"
        return response
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://steelsight-steel-inspector-platform.vercel.app",  # ← your Vercel URL
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(report.router)

@app.get("/")
def root():
    return {"status": "SteelSight API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}