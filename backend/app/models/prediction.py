"""
XGBoost Regression Model for Intervention Impact Prediction
"""
import numpy as np
import xgboost as xgb
from typing import Dict, List, Tuple
import json

class InterventionPredictor:
    """XGBoost model for predicting intervention impact"""
    
    def __init__(self):
        self.model = None
        self.is_fitted = False
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the XGBoost model"""
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            objective='reg:squarederror'
        )
        # For demo purposes, we'll use a pre-computed model behavior
        # In production, this would be loaded from a trained model file
        self.is_fitted = True
    
    def _simulate_intervention_impact(
        self,
        intervention_type: str,
        count: int,
        area: float,
        base_temp: float,
        lat: float,
        lon: float
    ) -> Dict:
        """
        Simulate the impact of an intervention based on type and parameters.
        This uses rule-based logic to simulate a fine-tuned model.
        """
        # Realistic impact coefficients (localized impact, not city-wide)
        # These represent LOCAL temperature reduction in the immediate area
        impact_coefficients = {
            "trees": {
                "temp_reduction": 0.08,  # degrees per tree (localized, realistic)
                "energy_saving": 0.03,   # MWh per tree per year
                "co2_reduction": 0.02,   # kg CO2 per tree per year
                "health_score": 0.05     # points per tree
            },
            "cool_roof": {
                "temp_reduction": 0.12,  # degrees per 100m² (localized)
                "energy_saving": 0.08,   # MWh per 100m² per year
                "co2_reduction": 0.05,   # kg per 100m² per year
                "health_score": 0.08     # points per 100m²
            },
            "park": {
                "temp_reduction": 0.20,  # degrees per 100m² (localized, parks have larger impact)
                "energy_saving": 0.05,   # MWh per 100m² per year
                "co2_reduction": 0.08,   # kg per 100m² per year
                "health_score": 0.12     # points per 100m²
            },
            "green_roof": {
                "temp_reduction": 0.15,  # degrees per 100m² (localized)
                "energy_saving": 0.06,   # MWh per 100m² per year
                "co2_reduction": 0.04,   # kg per 100m² per year
                "health_score": 0.10     # points per 100m²
            }
        }
        
        coeffs = impact_coefficients.get(intervention_type, impact_coefficients["trees"])
        
        # Calculate impact based on intervention type
        if intervention_type == "trees":
            # For trees, impact is based on count (with diminishing returns)
            # First 10 trees have full impact, then 80% for next 10, then 60%
            effective_count = min(count, 10) + min(max(0, count - 10), 10) * 0.8 + max(0, count - 20) * 0.6
            temp_reduction = coeffs["temp_reduction"] * effective_count
            energy_saving = coeffs["energy_saving"] * count
            co2_reduction = coeffs["co2_reduction"] * count
            health_score = coeffs["health_score"] * count
        else:
            # For area-based interventions, use area with diminishing returns
            # Impact scales with square root to represent localized effect
            area_factor = np.sqrt(area / 100)  # More realistic scaling
            temp_reduction = coeffs["temp_reduction"] * area_factor
            energy_saving = coeffs["energy_saving"] * (area / 100)
            co2_reduction = coeffs["co2_reduction"] * (area / 100)
            health_score = coeffs["health_score"] * (area / 100)
        
        # Add some randomness to simulate model uncertainty (with fixed seed for reproducibility)
        np.random.seed(int(lat * 100 + lon * 100) % 1000)  # Deterministic based on location
        noise_factor = 0.05  # Reduced noise for more consistent results
        temp_reduction *= (1 + np.random.uniform(-noise_factor, noise_factor))
        energy_saving *= (1 + np.random.uniform(-noise_factor, noise_factor))
        co2_reduction *= (1 + np.random.uniform(-noise_factor, noise_factor))
        health_score *= (1 + np.random.uniform(-noise_factor, noise_factor))
        
        # Ensure positive values
        temp_reduction = max(0, temp_reduction)
        energy_saving = max(0, energy_saving)
        co2_reduction = max(0, co2_reduction)
        health_score = max(0, health_score)
        
        return {
            "temperature_reduction": round(temp_reduction, 2),
            "energy_saving": round(energy_saving, 2),
            "co2_reduction": round(co2_reduction, 2),
            "health_score_improvement": round(health_score, 2)
        }
    
    def predict_intervention_impact(
        self,
        interventions: List[Dict]
    ) -> Dict:
        """
        Predict the cumulative impact of multiple interventions.
        Uses realistic localized impact calculations.
        
        Args:
            interventions: List of intervention dicts with keys:
                - type: str (trees, cool_roof, park, green_roof)
                - count: int (for trees)
                - area: float (for area-based interventions)
                - location: [lat, lon]
                - base_temperature: float
        
        Returns:
            Dict with cumulative impact metrics
        """
        if not interventions:
            return {
                "average_temperature": 38.5,
                "temperature_reduction": 0,
                "energy_saving": 0,
                "co2_reduction": 0,
                "health_score": 7.2,
                "intervention_count": 0
            }
        
        total_temp_reduction = 0
        total_energy_saving = 0
        total_co2_reduction = 0
        total_health_score = 0
        
        # Get baseline average temperature
        base_temps = [i.get("base_temperature", 35) for i in interventions]
        base_avg_temp = np.mean(base_temps) if base_temps else 35
        
        for intervention in interventions:
            impact = self._simulate_intervention_impact(
                intervention_type=intervention.get("type", "trees"),
                count=intervention.get("count", 0),
                area=intervention.get("area", 0),
                base_temp=intervention.get("base_temperature", 35),
                lat=intervention.get("location", [18.5204, 73.8567])[0],
                lon=intervention.get("location", [18.5204, 73.8567])[1]
            )
            
            total_temp_reduction += impact["temperature_reduction"]
            total_energy_saving += impact["energy_saving"]
            total_co2_reduction += impact["co2_reduction"]
            total_health_score += impact["health_score_improvement"]
        
        # Calculate city-wide average temperature reduction
        # Interventions have localized impact, so city-wide reduction is smaller
        # Scale down by factor based on number of interventions (more interventions = more coverage)
        coverage_factor = min(1.0, len(interventions) * 0.15)  # Max 15% city coverage per intervention
        city_wide_temp_reduction = total_temp_reduction * coverage_factor
        
        # New average temperature (realistic city-wide impact)
        new_avg_temp = max(25, base_avg_temp - city_wide_temp_reduction)  # Ensure reasonable minimum
        
        return {
            "average_temperature": round(new_avg_temp, 1),
            "temperature_reduction": round(city_wide_temp_reduction, 2),
            "energy_saving": round(total_energy_saving, 2),
            "co2_reduction": round(total_co2_reduction, 2),
            "health_score": round(min(10, max(5, 7.2 + total_health_score)), 1),  # Scale to 5-10
            "intervention_count": len(interventions)
        }

# Singleton instance
_predictor = None

def get_predictor() -> InterventionPredictor:
    """Get singleton predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = InterventionPredictor()
    return _predictor

