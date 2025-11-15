"""
Recommendations API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.services.recommendation_service import get_recommendation_service
from app.services.weather_service import get_weather_service

router = APIRouter()

@router.get("/recommendations")
async def get_recommendations() -> List[Dict]:
    """
    Get AI-generated recommendations for UHI mitigation.
    Returns list of actionable interventions.
    Optimized with smaller grid and caching.
    """
    try:
        recommendation_service = get_recommendation_service()
        weather_service = get_weather_service()
        
        # Reduced grid size from 20 to 12 for faster response (144 points instead of 400)
        heatmap_data = weather_service.get_heatmap_data(grid_size=12)
        
        # Generate recommendations
        recommendations = recommendation_service.generate_recommendations(heatmap_data)
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {str(e)}")


