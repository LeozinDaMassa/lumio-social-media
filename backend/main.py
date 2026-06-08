from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.supabase import supabase
from routes.auth import router as auth_router

app = FastAPI(title="Lumio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return {"status": "ok", "app": "Lumio"}

@app.get("/test-db")
def test_db():
    result = supabase.table("profiles").select("*").execute()
    return {"connection": "success", "data": result.data}
