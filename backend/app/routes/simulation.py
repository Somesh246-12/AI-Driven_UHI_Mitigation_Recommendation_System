"""
Simulation API Routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.models.prediction import get_predictor
from app.services.weather_service import get_weather_service
from app.services.health_service import get_health_service

router = APIRouter()

class Intervention(BaseModel):
    type: str  # trees, cool_roof, park, green_roof
    count: Optional[int] = 0
    area: Optional[float] = 0
    location: List[float]  # [lat, lon]
    base_temperature: Optional[float] = None

class SimulationRequest(BaseModel):
    interventions: List[Intervention]

class SimulationResponse(BaseModel):
    average_temperature: float
    temperature_reduction: float
    energy_saving: float
    co2_reduction: float
    health_score: float
    intervention_count: int

@router.post("/simulate_intervention", response_model=SimulationResponse)
async def simulate_intervention(request: SimulationRequest) -> SimulationResponse:
    """
    Simulate the impact of interventions on UHI.
    Returns predicted impact metrics.
    """
    try:
        predictor = get_predictor()
        weather_service = get_weather_service()
        health_service = get_health_service()
        
        # Convert interventions to dict format
        # Optimized: batch process weather data if needed
        interventions = []
        base_temps = []
        air_qualities = []
        
        # Cache weather lookups to avoid redundant calculations
        weather_cache = {}
        
        for intervention in request.interventions:
            # Get base temperature and air quality for location if not provided
            base_temp = intervention.base_temperature
            air_quality = "moderate"
            
            if base_temp is None:
                # Use cached location key to avoid redundant calculations
                loc_key = (round(intervention.location[0], 4), round(intervention.location[1], 4))
                if loc_key not in weather_cache:
                    weather = weather_service.get_current_weather(
                        intervention.location[0],
                        intervention.location[1]
                    )
                    weather_cache[loc_key] = weather
                else:
                    weather = weather_cache[loc_key]
                
                base_temp = weather["temperature"]
                air_quality = weather["air_quality"]
            
            base_temps.append(base_temp)
            air_qualities.append(air_quality)
            
            interventions.append({
                "type": intervention.type,
                "count": intervention.count or 0,
                "area": intervention.area or 0,
                "location": intervention.location,
                "base_temperature": base_temp
            })
        
        # Predict impact
        impact = predictor.predict_intervention_impact(interventions)
        
        # Calculate health score using health service
        avg_temp = impact["average_temperature"]
        avg_air_quality = max(set(air_qualities), key=air_qualities.count) if air_qualities else "moderate"
        health_score = health_service.get_health_score(
            temperature=avg_temp,
            air_quality=avg_air_quality,
            interventions=interventions
        )
        
        impact["health_score"] = health_score
        
        return SimulationResponse(**impact)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulating intervention: {str(e)}")


