from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyse import router as analyse_router
from routes.insights import router as insights_router

app = FastAPI(title="AI analytics backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Health check route
@app.get("/")
def health():
    return {"status": "App is running 🚀"}

# 🔹 Routers
app.include_router(analyse_router, prefix="/api")
app.include_router(insights_router, prefix="/api")
