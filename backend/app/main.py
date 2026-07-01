from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from app.routers import auth, predict, report
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

security = HTTPBearer()

app = FastAPI(
    title="SteelSight API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://steel-sight-steel-inspector-platfor.vercel.app",  # ← add after Vercel deploy
    ],
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