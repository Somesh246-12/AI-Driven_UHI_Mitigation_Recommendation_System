"""
Health Precautions Service based on real climate data
"""
from typing import List, Dict
from app.services.weather_service import get_weather_service

class HealthService:
    """Service for generating health precautions based on climate data"""
    
    def __init__(self):
        self.weather_service = get_weather_service()
    
    def get_health_precautions(self, lat: float = None, lon: float = None) -> List[Dict]:
        """
        Get health precautions based on real-time weather conditions.
        Uses live climate data to generate contextual, location-aware advice.
        """
        weather = self.weather_service.get_current_weather(lat, lon)
        temperature = weather["temperature"]
        air_quality = weather["air_quality"]
        humidity = weather["humidity"]
        
        # Calculate heat index (feels-like temperature)
        heat_index = self._calculate_heat_index(temperature, humidity)
        
        precautions = []
        
        # Heat index-based precautions (more accurate than temperature alone)
        if heat_index > 45:
            precautions.append({
                "id": 1,
                "type": "extreme_heat_danger",
                "title": "Extreme Heat Danger",
                "message": f"Feels like {heat_index}°C (actual: {temperature}°C). Life-threatening conditions. Stay indoors.",
                "severity": "high",
                "recommendations": [
                    "Stay indoors in air-conditioned spaces immediately",
                    "Drink water every 15-20 minutes (3-4 liters per day)",
                    "Wear loose, light-colored, breathable clothing",
                    "Avoid ALL outdoor activities",
                    "Check on elderly, children, and vulnerable individuals every 2 hours",
                    "Seek medical attention if experiencing dizziness, nausea, or confusion"
                ]
            })
        elif heat_index > 40 or temperature > 40:
            precautions.append({
                "id": 1,
                "type": "extreme_heat",
                "title": "Extreme Heat Warning",
                "message": f"Temperature is {temperature}°C. Avoid outdoor activities during peak hours (11 AM - 4 PM).",
                "severity": "high",
                "recommendations": [
                    "Stay indoors in air-conditioned spaces",
                    "Drink plenty of water (at least 2-3 liters per day)",
                    "Wear loose, light-colored clothing",
                    "Avoid strenuous physical activities",
                    "Check on elderly and vulnerable individuals"
                ]
            })
        elif temperature > 38:
            precautions.append({
                "id": 2,
                "type": "high_heat",
                "title": "High Heat Alert",
                "message": f"Temperature is {temperature}°C. Take precautions when outdoors.",
                "severity": "medium",
                "recommendations": [
                    "Limit outdoor activities to early morning or evening",
                    "Stay hydrated throughout the day",
                    "Wear sunscreen and protective clothing",
                    "Take frequent breaks in shaded areas",
                    "Avoid direct sun exposure during midday"
                ]
            })
        elif temperature > 35:
            precautions.append({
                "id": 3,
                "type": "moderate_heat",
                "title": "Moderate Heat Advisory",
                "message": f"Temperature is {temperature}°C. Stay cool and hydrated.",
                "severity": "low",
                "recommendations": [
                    "Drink water regularly",
                    "Wear light clothing",
                    "Seek shade when possible",
                    "Monitor for signs of heat exhaustion"
                ]
            })
        
        # Air quality-based precautions
        if air_quality == "poor":
            precautions.append({
                "id": 4,
                "type": "poor_air_quality",
                "title": "Poor Air Quality Alert",
                "message": "Air quality is poor. Limit outdoor activities, especially for sensitive groups.",
                "severity": "high",
                "recommendations": [
                    "Avoid outdoor exercise",
                    "Keep windows closed",
                    "Use air purifiers if available",
                    "Wear N95 masks if going outside",
                    "Children, elderly, and people with respiratory conditions should stay indoors"
                ]
            })
        elif air_quality == "moderate":
            precautions.append({
                "id": 5,
                "type": "moderate_air_quality",
                "title": "Moderate Air Quality",
                "message": "Air quality is moderate. Sensitive individuals should take precautions.",
                "severity": "medium",
                "recommendations": [
                    "Limit prolonged outdoor activities",
                    "Avoid heavy exercise outdoors",
                    "Sensitive groups should reduce outdoor exposure",
                    "Keep indoor air clean with proper ventilation"
                ]
            })
        
        # Humidity-based precautions
        if humidity > 70 and temperature > 35:
            precautions.append({
                "id": 6,
                "type": "high_humidity",
                "title": "High Humidity Warning",
                "message": f"High humidity ({humidity}%) combined with heat increases heat index.",
                "severity": "medium",
                "recommendations": [
                    "Heat feels more intense due to high humidity",
                    "Increase fluid intake",
                    "Take cool showers to lower body temperature",
                    "Use fans or air conditioning",
                    "Avoid excessive physical activity"
                ]
            })
        
        # General urban heat island precautions
        precautions.append({
            "id": 7,
            "type": "uhi_general",
            "title": "Urban Heat Island Effects",
            "message": "Urban areas can be 2-5°C hotter than surrounding areas.",
            "severity": "low",
            "recommendations": [
                "Seek green spaces and parks for relief",
                "Use public transportation to reduce heat emissions",
                "Support tree planting initiatives",
                "Use reflective materials for buildings",
                "Advocate for more urban green infrastructure"
            ]
        })
        
        return precautions
    
    def _calculate_heat_index(self, temperature: float, humidity: float) -> float:
        """
        Calculate heat index (feels-like temperature) using Rothfusz equation.
        More accurate representation of how hot it actually feels.
        """
        # Convert to Fahrenheit for calculation (Rothfusz equation uses F)
        temp_f = (temperature * 9/5) + 32
        rh = humidity
        
        # Rothfusz regression equation
        hi = (
            0.5 * (temp_f + 61.0 + ((temp_f - 68.0) * 1.2) + (rh * 0.094))
        )
        
        # Adjustments for higher temperatures
        if temp_f >= 80:
            hi = (
                -42.379 + 
                2.04901523 * temp_f + 
                10.14333127 * rh - 
                0.22475541 * temp_f * rh - 
                6.83783e-3 * temp_f**2 - 
                5.481717e-2 * rh**2 + 
                1.22874e-3 * temp_f**2 * rh + 
                8.5282e-4 * temp_f * rh**2 - 
                1.99e-6 * temp_f**2 * rh**2
            )
        
        # Convert back to Celsius
        hi_c = (hi - 32) * 5/9
        return round(hi_c, 1)
    
    def get_health_score(self, temperature: float, air_quality: str, interventions: List[Dict] = None) -> float:
        """
        Calculate health score based on environmental conditions and interventions.
        Score ranges from 0-10.
        """
        base_score = 5.0
        
        # Temperature impact
        if temperature > 40:
            base_score -= 2.5
        elif temperature > 38:
            base_score -= 1.5
        elif temperature > 35:
            base_score -= 0.5
        elif temperature < 30:
            base_score += 0.5
        
        # Air quality impact
        if air_quality == "poor":
            base_score -= 1.5
        elif air_quality == "moderate":
            base_score -= 0.5
        elif air_quality == "good":
            base_score += 0.5
        
        # Intervention impact
        if interventions:
            for intervention in interventions:
                if intervention.get("type") == "trees":
                    base_score += 0.1 * intervention.get("count", 0) / 10
                elif intervention.get("type") == "park":
                    base_score += 0.2 * (intervention.get("area", 0) / 1000)
                elif intervention.get("type") in ["cool_roof", "green_roof"]:
                    base_score += 0.15 * (intervention.get("area", 0) / 1000)
        
        # Ensure score is within 0-10 range
        return max(0, min(10, round(base_score, 1)))

# Singleton instance
_health_service = None

def get_health_service() -> HealthService:
    """Get singleton health service instance"""
    global _health_service
    if _health_service is None:
        _health_service = HealthService()
    return _health_service


