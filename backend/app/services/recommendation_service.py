"""
AI Recommendation Service for UHI Mitigation Strategies
"""
from typing import List, Dict
import numpy as np
from app.services.weather_service import get_weather_service

class RecommendationService:
    """Service for generating AI-driven recommendations"""
    
    def __init__(self):
        self.weather_service = get_weather_service()
    
    def generate_recommendations(self, heatmap_data: Dict = None) -> List[Dict]:
        """
        Generate AI-driven recommendations based on real-time heatmap data.
        Analyzes hotspots and provides diverse, contextual interventions.
        """
        recommendations = []
        
        # Analyze heatmap data to identify hotspots
        if heatmap_data and "features" in heatmap_data:
            features = heatmap_data["features"]
            if not features:
                return self._get_default_recommendations()
                
            temperatures = [f["properties"]["temperature"] for f in features]
            avg_temp = np.mean(temperatures)
            max_temp = max(temperatures)
            min_temp = min(temperatures)
            temp_range = max_temp - min_temp
            
            # Find hottest areas (top 20% of temperatures)
            temp_threshold = avg_temp + (temp_range * 0.3)
            hot_features = [f for f in features if f["properties"]["temperature"] >= temp_threshold]
            
            # Sort by temperature (hottest first)
            hot_features.sort(key=lambda x: x["properties"]["temperature"], reverse=True)
            
            # Generate diverse recommendations based on temperature patterns
            intervention_types = []
            
            # High priority: Very hot areas (>38°C)
            if max_temp > 38:
                for i, feature in enumerate(hot_features[:4]):
                    props = feature["properties"]
                    temp = props["temperature"]
                    
                    # Vary recommendations based on temperature severity
                    if temp > 40:
                        # Extreme heat - recommend parks (largest impact)
                        recommendations.append({
                            "id": len(recommendations) + 1,
                            "action": "Create urban park",
                            "description": f"Convert area into green space. Current temp: {temp}°C. Expected reduction: {round((temp - avg_temp) * 0.35, 1)}°C",
                            "location": {
                                "lat": props["lat"],
                                "lon": props["lon"],
                                "address": f"Critical Hotspot {i+1} ({temp}°C)"
                            },
                            "priority": "High",
                            "estimated_impact": {
                                "temp_reduction": round((temp - avg_temp) * 0.35, 1),
                                "cost": "Medium",
                                "timeframe": "6-12 months"
                            },
                            "type": "park",
                            "area": 1500 + (i * 200)  # Vary park sizes
                        })
                    elif temp > 39:
                        # Very hot - recommend tree planting
                        tree_count = 25 + (i * 5)
                        recommendations.append({
                            "id": len(recommendations) + 1,
                            "action": "Plant urban forest",
                            "description": f"Plant {tree_count} trees to create canopy cover. Current temp: {temp}°C",
                            "location": {
                                "lat": props["lat"],
                                "lon": props["lon"],
                                "address": f"Hotspot Zone {i+1} ({temp}°C)"
                            },
                            "priority": "High",
                            "estimated_impact": {
                                "temp_reduction": round((temp - avg_temp) * 0.32, 1),
                                "cost": "Low",
                                "timeframe": "3-6 months"
                            },
                            "type": "trees",
                            "count": tree_count
                        })
                    else:
                        # Hot - recommend cool roofs
                        recommendations.append({
                            "id": len(recommendations) + 1,
                            "action": "Install cool roof system",
                            "description": f"Apply reflective coating to buildings. Current temp: {temp}°C",
                            "location": {
                                "lat": props["lat"],
                                "lon": props["lon"],
                                "address": f"Building Zone {i+1} ({temp}°C)"
                            },
                            "priority": "High",
                            "estimated_impact": {
                                "temp_reduction": round((temp - avg_temp) * 0.28, 1),
                                "cost": "Medium",
                                "timeframe": "1-2 months"
                            },
                            "type": "cool_roof",
                            "area": 600 + (i * 100)
                        })
            
            # Medium priority: Moderately hot areas (35-38°C)
            if avg_temp > 35 and len(hot_features) > 4:
                for i, feature in enumerate(hot_features[4:7]):
                    props = feature["properties"]
                    temp = props["temperature"]
                    
                    # Alternate between intervention types
                    if i % 2 == 0:
                        recommendations.append({
                            "id": len(recommendations) + 1,
                            "action": "Install green roof",
                            "description": f"Convert rooftop to vegetation. Current temp: {temp}°C",
                            "location": {
                                "lat": props["lat"],
                                "lon": props["lon"],
                                "address": f"Rooftop Zone {i+1} ({temp}°C)"
                            },
                            "priority": "Medium",
                            "estimated_impact": {
                                "temp_reduction": round((temp - avg_temp) * 0.22, 1),
                                "cost": "High",
                                "timeframe": "2-4 months"
                            },
                            "type": "green_roof",
                            "area": 500 + (i * 50)
                        })
                    else:
                        recommendations.append({
                            "id": len(recommendations) + 1,
                            "action": "Plant shade trees",
                            "description": f"Plant {20 + (i * 3)} trees along streets. Current temp: {temp}°C",
                            "location": {
                                "lat": props["lat"],
                                "lon": props["lon"],
                                "address": f"Street Zone {i+1} ({temp}°C)"
                            },
                            "priority": "Medium",
                            "estimated_impact": {
                                "temp_reduction": round((temp - avg_temp) * 0.25, 1),
                                "cost": "Low",
                                "timeframe": "3-6 months"
                            },
                            "type": "trees",
                            "count": 20 + (i * 3)
                        })
            
            # Add strategic recommendations based on overall heat distribution
            if temp_range > 5:
                # High variation - recommend targeted interventions
                mid_temp_features = [f for f in features if avg_temp - 1 <= f["properties"]["temperature"] <= avg_temp + 1]
                if mid_temp_features:
                    feature = mid_temp_features[0]
                    props = feature["properties"]
                    recommendations.append({
                        "id": len(recommendations) + 1,
                        "action": "Create cooling corridor",
                        "description": "Connect green spaces to create cooling pathways",
                        "location": {
                            "lat": props["lat"],
                            "lon": props["lon"],
                            "address": "Strategic Location"
                        },
                        "priority": "Medium",
                        "estimated_impact": {
                            "temp_reduction": round(temp_range * 0.15, 1),
                            "cost": "Medium",
                            "timeframe": "6-12 months"
                        },
                        "type": "park",
                        "area": 1000
                    })
        
        # Add some default recommendations if none generated
        if not recommendations:
            recommendations = self._get_default_recommendations()
        
        # Sort by priority and impact
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        recommendations.sort(key=lambda x: (
            priority_order.get(x["priority"], 3),
            -x["estimated_impact"]["temp_reduction"]  # Higher reduction first
        ))
        
        return recommendations[:8]  # Return top 8 for better UX
    
    def _get_default_recommendations(self) -> List[Dict]:
        """Get default recommendations for Pune"""
        return [
            {
                "id": 1,
                "action": "Plant trees",
                "description": "Plant 30 trees along Main Street to create urban canopy",
                "location": {
                    "lat": 18.5204,
                    "lon": 73.8567,
                    "address": "City Center, Pune"
                },
                "priority": "High",
                "estimated_impact": {
                    "temp_reduction": 3.5,
                    "cost": "Low",
                    "timeframe": "3-6 months"
                },
                "type": "trees",
                "count": 30
            },
            {
                "id": 2,
                "action": "Create park",
                "description": "Convert vacant lot into green space with trees and grass",
                "location": {
                    "lat": 18.5350,
                    "lon": 73.8400,
                    "address": "Commercial District, Pune"
                },
                "priority": "High",
                "estimated_impact": {
                    "temp_reduction": 4.2,
                    "cost": "Medium",
                    "timeframe": "6-12 months"
                },
                "type": "park",
                "area": 2000  # square meters
            },
            {
                "id": 3,
                "action": "Install cool roof",
                "description": "Apply reflective coating to commercial buildings",
                "location": {
                    "lat": 18.5100,
                    "lon": 73.8700,
                    "address": "Dense Residential Area, Pune"
                },
                "priority": "Medium",
                "estimated_impact": {
                    "temp_reduction": 2.8,
                    "cost": "Medium",
                    "timeframe": "1-2 months"
                },
                "type": "cool_roof",
                "area": 800
            },
            {
                "id": 4,
                "action": "Plant trees",
                "description": "Increase tree cover in residential neighborhoods",
                "location": {
                    "lat": 18.5500,
                    "lon": 73.8200,
                    "address": "Suburban Area, Pune"
                },
                "priority": "Medium",
                "estimated_impact": {
                    "temp_reduction": 2.5,
                    "cost": "Low",
                    "timeframe": "3-6 months"
                },
                "type": "trees",
                "count": 20
            },
            {
                "id": 5,
                "action": "Install green roof",
                "description": "Convert rooftop to green space with vegetation",
                "location": {
                    "lat": 18.4800,
                    "lon": 73.8900,
                    "address": "Peri-urban Area, Pune"
                },
                "priority": "Low",
                "estimated_impact": {
                    "temp_reduction": 2.0,
                    "cost": "High",
                    "timeframe": "2-4 months"
                },
                "type": "green_roof",
                "area": 600
            }
        ]

# Singleton instance
_recommendation_service = None

def get_recommendation_service() -> RecommendationService:
    """Get singleton recommendation service instance"""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    return _recommendation_service


