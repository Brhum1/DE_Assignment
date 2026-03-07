from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, projects, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + Vite Project")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # رابط مشروع Vite الافتراضي
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ربط المسارات (Include Routers)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def root():
    return {"message": "Server is running successfully!"}