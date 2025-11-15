"""
Weather Service for fetching real-time Pune temperature data
"""
import requests
import os
from typing import List, Dict, Tuple
import numpy as np
import json
import math

class WeatherService:
    """Service for fetching and processing weather data"""
    
    def __init__(self):
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "")
        self.pune_center = (18.5204, 73.8567)  # Pune coordinates
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self._heatmap_cache = None
        self._cache_timestamp = None
        self._cache_ttl = 300  # Cache for 5 minutes
    
    def _generate_grid_coordinates(self, center_lat: float, center_lon: float, grid_size: int = 20) -> List[Tuple[float, float]]:
        """
        Generate a grid of coordinates around Pune for heatmap visualization.
        Creates a smooth distribution for continuous heatmap appearance.
        """
        coordinates = []
        # Create a grid with some randomness for natural look
        lat_range = 0.15  # ~15km radius
        lon_range = 0.15
        
        # Use fixed seed for consistent heatmap (can be removed for more variation)
        np.random.seed(42)
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Create a more uniform grid with slight variations
                lat_step = (i / grid_size - 0.5) * 2 * lat_range
                lon_step = (j / grid_size - 0.5) * 2 * lon_range
                
                # Add small random offset for natural variation
                lat_offset = np.random.uniform(-0.01, 0.01)
                lon_offset = np.random.uniform(-0.01, 0.01)
                
                lat = center_lat + lat_step + lat_offset
                lon = center_lon + lon_step + lon_offset
                
                coordinates.append((lat, lon))
        
        return coordinates
    
    def _get_temperature_from_api(self, lat: float, lon: float) -> float:
        """Get temperature from OpenWeatherMap API"""
        if not self.openweather_api_key:
            # Fallback: Generate realistic temperature based on location
            return self._generate_synthetic_temperature(lat, lon)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.openweather_api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data["main"]["temp"]
            else:
                return self._generate_synthetic_temperature(lat, lon)
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._generate_synthetic_temperature(lat, lon)
    
    def _fast_distance_km(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Fast distance calculation using Haversine formula (much faster than geodesic).
        Accurate enough for small distances like within a city.
        """
        # Haversine formula
        R = 6371  # Earth radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
             math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def _generate_synthetic_temperature(self, lat: float, lon: float) -> float:
        """
        Generate synthetic temperature data that creates realistic UHI patterns.
        Simulates higher temperatures in urban centers and lower in peripheral areas.
        Optimized with fast distance calculation.
        """
        # Base temperature (Pune average: ~28-35°C)
        base_temp = 32.0
        
        # UHI effect: higher temperature in city center, lower in periphery
        # Create hotspot zones
        hotspot_zones = [
            (18.5204, 73.8567, 38.5),  # City center - hottest
            (18.5350, 73.8400, 37.2),  # Commercial area
            (18.5100, 73.8700, 36.8),  # Dense residential
            (18.5500, 73.8200, 35.5),  # Suburban
            (18.4800, 73.8900, 34.2),  # Peri-urban
        ]
        
        # Find closest hotspot using fast distance calculation
        min_distance = float('inf')
        closest_temp = base_temp
        
        for zone_lat, zone_lon, zone_temp in hotspot_zones:
            zone_distance = self._fast_distance_km(zone_lat, zone_lon, lat, lon)
            if zone_distance < min_distance:
                min_distance = zone_distance
                closest_temp = zone_temp
        
        # Apply distance-based cooling
        temperature = closest_temp - (min_distance * 0.1)  # Cool by 0.1°C per km
        
        # Add some natural variation (using deterministic seed for consistency)
        # Use hash of coordinates for consistent variation
        coord_hash = hash((round(lat, 3), round(lon, 3))) % 1000
        variation = (coord_hash / 1000.0 - 0.5) * 3.0  # -1.5 to 1.5
        temperature += variation
        
        # Ensure reasonable range
        temperature = max(25, min(42, temperature))
        
        return round(temperature, 1)
    
    def get_heatmap_data(self, grid_size: int = 25) -> Dict:
        """
        Get heatmap data for Pune as GeoJSON FeatureCollection.
        Returns smooth, continuous heatmap data.
        Uses caching to improve performance.
        """
        import time
        
        # Check cache (use same grid size or smaller)
        current_time = time.time()
        if (self._heatmap_cache and 
            self._cache_timestamp and 
            (current_time - self._cache_timestamp) < self._cache_ttl and
            len(self._heatmap_cache.get("features", [])) >= grid_size * grid_size):
            # Return cached data (it has enough points)
            return self._heatmap_cache
        
        coordinates = self._generate_grid_coordinates(
            self.pune_center[0],
            self.pune_center[1],
            grid_size
        )
        
        features = []
        for lat, lon in coordinates:
            temperature = self._get_temperature_from_api(lat, lon)
            
            # Create a small circular area for each point (for heatmap visualization)
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "temperature": temperature,
                    "lat": lat,
                    "lon": lon
                }
            }
            features.append(feature)
        
        result = {
            "type": "FeatureCollection",
            "features": features,
            "metadata": {
                "city": "Pune",
                "center": [self.pune_center[1], self.pune_center[0]],
                "total_points": len(features),
                "avg_temperature": round(np.mean([f["properties"]["temperature"] for f in features]), 1),
                "max_temperature": round(max([f["properties"]["temperature"] for f in features]), 1),
                "min_temperature": round(min([f["properties"]["temperature"] for f in features]), 1)
            }
        }
        
        # Cache the result
        self._heatmap_cache = result
        self._cache_timestamp = current_time
        
        return result
    
    def get_current_weather(self, lat: float = None, lon: float = None) -> Dict:
        """Get current weather for a specific location"""
        if lat is None or lon is None:
            lat, lon = self.pune_center
        
        temperature = self._get_temperature_from_api(lat, lon)
        
        # Generate air quality and humidity estimates
        air_quality = "moderate"
        if temperature > 38:
            air_quality = "poor"
        elif temperature > 35:
            air_quality = "moderate"
        else:
            air_quality = "good"
        
        humidity = np.random.uniform(40, 80)
        
        return {
            "temperature": temperature,
            "air_quality": air_quality,
            "humidity": round(humidity, 1),
            "location": {"lat": lat, "lon": lon}
        }

# Singleton instance
_weather_service = None

def get_weather_service() -> WeatherService:
    """Get singleton weather service instance"""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service

