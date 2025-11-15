"""
Health Precautions API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from app.services.health_service import get_health_service

router = APIRouter()

@router.get("/health_precautions")
async def get_health_precautions(
    lat: Optional[float] = None,
    lon: Optional[float] = None
) -> List[Dict]:
    """
    Get health precautions based on current climate data.
    Returns list of health recommendations.
    """
    try:
        health_service = get_health_service()
        precautions = health_service.get_health_precautions(lat, lon)
        return precautions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching health precautions: {str(e)}")


