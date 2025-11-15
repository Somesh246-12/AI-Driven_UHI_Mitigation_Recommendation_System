"""
Heatmap API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict
from app.services.weather_service import get_weather_service

router = APIRouter()

@router.get("/heatmap_data")
async def get_heatmap_data() -> Dict:
    """
    Get thermal heatmap data for Pune.
    Returns GeoJSON FeatureCollection with temperature data.
    Optimized with smaller grid for faster response.
    """
    try:
        weather_service = get_weather_service()
        # Reduced grid size from 30 to 15 for faster response (225 points instead of 900)
        heatmap_data = weather_service.get_heatmap_data(grid_size=15)
        return heatmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching heatmap data: {str(e)}")


