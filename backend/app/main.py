from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import heatmap, simulation, recommendations, health
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="UHI Mitigation API",
    description="AI-Driven Urban Heat Island Mitigation Recommendation System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(heatmap.router, prefix="/api/v1", tags=["Heatmap"])
app.include_router(simulation.router, prefix="/api/v1", tags=["Simulation"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["Recommendations"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "UHI Mitigation API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


