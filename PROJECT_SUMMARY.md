# AI-Driven Urban Heat Island (UHI) Mitigation Recommendation System

## Project Overview

This is a full-stack web application that maps urban heat islands in Pune, India, simulates mitigation strategies (trees, cool roofs, parks), and provides AI-driven recommendations to reduce heat.

## Key Features

1. **Interactive Thermal Heatmap**
   - Real-time temperature visualization of Pune using Mapbox GL JS
   - Smooth, continuous heatmap display (not discrete polygons)
   - Centered on Pune, India (18.5204°N, 73.8567°E)

2. **AI-Driven Hotspot Detection**
   - K-Means clustering to identify distinct UHI zones
   - Automatic severity classification (high, medium, low)

3. **Intervention Simulation**
   - XGBoost regression model to predict impact of mitigation strategies
   - Support for multiple intervention types:
     - Trees (count-based)
     - Cool Roofs (area-based)
     - Parks (area-based)
     - Green Roofs (area-based)

4. **Real-time Impact Dashboard**
   - Average Temperature
   - Temperature Reduction
   - Energy Savings (MWh)
   - CO2 Reduction (kg)
   - Public Health Score (0-10)

5. **AI Recommendations**
   - Prioritized recommendations based on heatmap analysis
   - Actionable interventions with estimated impact
   - Cost and timeframe estimates

6. **Health Precautions**
   - AI-recommended health advice based on real climate data
   - Temperature-based warnings
   - Air quality advisories
   - Humidity alerts

## Technical Stack

### Backend
- **Framework**: FastAPI (Python)
- **ML Models**: scikit-learn (K-Means), XGBoost
- **Data Processing**: NumPy, Pandas
- **Geospatial**: GeoPy, Shapely
- **API**: RESTful API with JSON responses

### Frontend
- **Framework**: React.js (Functional Components with Hooks)
- **Mapping**: Mapbox GL JS (react-map-gl)
- **Styling**: CSS Modules
- **State Management**: React Context API
- **HTTP Client**: Axios

### Data
- **Real-time Data**: Pune temperature data (synthetic or OpenWeatherMap API)
- **Format**: GeoJSON FeatureCollection
- **Storage**: In-memory (can be extended to MongoDB)

## Project Structure

```
UHI/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models/              # ML models
│   │   │   ├── clustering.py    # K-Means clustering
│   │   │   └── prediction.py    # XGBoost regression
│   │   ├── routes/              # API routes
│   │   │   ├── heatmap.py       # Heatmap data endpoint
│   │   │   ├── simulation.py    # Simulation endpoint
│   │   │   ├── recommendations.py # Recommendations endpoint
│   │   │   └── health.py        # Health precautions endpoint
│   │   └── services/            # Business logic
│   │       ├── weather_service.py      # Weather data service
│   │       ├── recommendation_service.py # Recommendation service
│   │       └── health_service.py       # Health service
│   ├── requirements.txt
│   ├── .env.example
│   └── run.py                   # Quick start script
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Sidebar.js       # Navigation sidebar
│   │   │   ├── Header.js        # Header with theme toggle
│   │   │   ├── MapContainer.js  # Interactive map
│   │   │   ├── ImpactDashboard.js # Impact metrics
│   │   │   ├── StatCard.js      # Stat card component
│   │   │   ├── RecommendationList.js # Recommendations list
│   │   │   └── HealthPrecautions.js # Health precautions
│   │   ├── contexts/
│   │   │   └── ThemeContext.js  # Theme context
│   │   ├── services/
│   │   │   └── api.js           # API service
│   │   ├── App.js               # Main app component
│   │   └── index.js             # Entry point
│   ├── package.json
│   └── .env.example
├── README.md
├── SETUP.md
└── .gitignore
```

## API Endpoints

### 1. GET /api/v1/heatmap_data
Returns thermal heatmap data for Pune as GeoJSON FeatureCollection.

**Response:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [lon, lat]
      },
      "properties": {
        "temperature": 38.5,
        "lat": 18.5204,
        "lon": 73.8567
      }
    }
  ],
  "metadata": {
    "city": "Pune",
    "center": [73.8567, 18.5204],
    "total_points": 625,
    "avg_temperature": 35.2,
    "max_temperature": 39.8,
    "min_temperature": 30.5
  }
}
```

### 2. POST /api/v1/simulate_intervention
Simulates the impact of interventions on UHI.

**Request:**
```json
{
  "interventions": [
    {
      "type": "trees",
      "count": 20,
      "area": 0,
      "location": [18.5204, 73.8567],
      "base_temperature": 35
    }
  ]
}
```

**Response:**
```json
{
  "average_temperature": 33.5,
  "temperature_reduction": 1.5,
  "energy_saving": 1.2,
  "co2_reduction": 850,
  "health_score": 7.8,
  "intervention_count": 1
}
```

### 3. GET /api/v1/recommendations
Returns AI-generated recommendations for UHI mitigation.

**Response:**
```json
[
  {
    "id": 1,
    "action": "Plant trees",
    "description": "Plant 30 trees along Main Street",
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
  }
]
```

### 4. GET /api/v1/health_precautions
Returns health precautions based on current climate data.

**Response:**
```json
[
  {
    "id": 1,
    "type": "extreme_heat",
    "title": "Extreme Heat Warning",
    "message": "Temperature is 40°C. Avoid outdoor activities.",
    "severity": "high",
    "recommendations": [
      "Stay indoors in air-conditioned spaces",
      "Drink plenty of water"
    ]
  }
]
```

## ML Models

### 1. K-Means Clustering (Hotspot Detection)
- **Purpose**: Identify distinct UHI hotspot zones
- **Implementation**: scikit-learn KMeans
- **Parameters**: n_clusters=5, random_state=42
- **Features**: Latitude, Longitude, Temperature
- **Output**: Cluster assignments with severity classification

### 2. XGBoost Regression (Impact Prediction)
- **Purpose**: Predict impact of interventions
- **Implementation**: XGBoost XGBRegressor
- **Parameters**: n_estimators=100, max_depth=6, learning_rate=0.1
- **Features**: Intervention type, count/area, location, base temperature
- **Output**: Temperature reduction, energy savings, CO2 reduction, health score

## How to Run

1. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   python run.py
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   cp .env.example .env
   # Edit .env with your Mapbox token
   npm start
   ```

3. **Access:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Demo Flow

1. **View Heatmap**: Open the application to see the thermal heatmap of Pune
2. **Add Interventions**: Click on map tools to add interventions (trees, cool roofs, parks)
3. **Simulate Impact**: Click "Simulate" to see predicted impact metrics
4. **View Recommendations**: Check the AI recommendations panel for suggested actions
5. **Health Precautions**: Scroll down to see health precautions based on climate data

## Future Enhancements

1. **Real-time Data Integration**: Integrate with OpenWeatherMap API for live data
2. **Database Storage**: Store interventions and scenarios in MongoDB
3. **User Authentication**: Add user login and session management
4. **Historical Data**: Track temperature changes over time
5. **Advanced ML Models**: Fine-tune models with real historical data
6. **Export Features**: Export reports and visualizations
7. **Mobile App**: Create a mobile version of the application

## License

MIT


