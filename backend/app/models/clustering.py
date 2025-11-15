"""
K-Means Clustering Model for UHI Hotspot Detection
"""
import numpy as np
from sklearn.cluster import KMeans
from typing import List, Tuple, Dict
import json

class UHIClusterer:
    """K-Means clustering model for identifying UHI hotspots"""
    
    def __init__(self, n_clusters: int = 5):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.is_fitted = False
        
    def fit(self, coordinates: List[Tuple[float, float]], temperatures: List[float]):
        """Fit the clustering model on coordinates and temperatures"""
        X = np.array([[coord[0], coord[1], temp] for coord, temp in zip(coordinates, temperatures)])
        self.model.fit(X)
        self.is_fitted = True
        return self
    
    def predict_hotspot(self, lat: float, lon: float, temperature: float) -> int:
        """Predict which hotspot cluster a location belongs to"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        X = np.array([[lat, lon, temperature]])
        return self.model.predict(X)[0]
    
    def get_hotspot_zones(self, coordinates: List[Tuple[float, float]], temperatures: List[float]) -> Dict:
        """Get all hotspot zones with their characteristics"""
        if not self.is_fitted:
            self.fit(coordinates, temperatures)
        
        predictions = self.model.predict(
            np.array([[coord[0], coord[1], temp] for coord, temp in zip(coordinates, temperatures)])
        )
        
        zones = {}
        for i in range(self.n_clusters):
            cluster_points = [j for j, pred in enumerate(predictions) if pred == i]
            if cluster_points:
                cluster_temps = [temperatures[j] for j in cluster_points]
                cluster_coords = [coordinates[j] for j in cluster_points]
                
                zones[i] = {
                    "cluster_id": i,
                    "avg_temperature": np.mean(cluster_temps),
                    "max_temperature": np.max(cluster_temps),
                    "min_temperature": np.min(cluster_temps),
                    "center": [
                        np.mean([c[0] for c in cluster_coords]),
                        np.mean([c[1] for c in cluster_coords])
                    ],
                    "point_count": len(cluster_points),
                    "severity": "high" if np.mean(cluster_temps) > 38 else "medium" if np.mean(cluster_temps) > 35 else "low"
                }
        
        return zones

# Singleton instance
_uhi_clusterer = None

def get_clusterer() -> UHIClusterer:
    """Get singleton clusterer instance"""
    global _uhi_clusterer
    if _uhi_clusterer is None:
        _uhi_clusterer = UHIClusterer(n_clusters=5)
    return _uhi_clusterer


