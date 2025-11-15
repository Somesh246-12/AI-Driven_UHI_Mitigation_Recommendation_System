# AI-Driven Urban Heat Island (UHI) Mitigation Recommendation System

A full-stack web application that maps urban heat islands in Pune, India, simulates mitigation strategies (trees, cool roofs, parks), and provides AI-driven recommendations to reduce heat.

## Project Structure

```
UHI/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # ML models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── .env.example
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── styles/         # CSS modules
│   │   └── App.js
│   ├── package.json
│   └── public/
└── README.md
```

## Features

- **Interactive Thermal Heatmap**: Real-time temperature visualization of Pune using Mapbox GL JS
- **AI-Driven Hotspot Detection**: K-Means clustering to identify UHI zones
- **Intervention Simulation**: XGBoost model to predict impact of mitigation strategies
- **Real-time Recommendations**: AI-generated actionable interventions
- **Impact Dashboard**: Temperature reduction, energy savings, CO2 reduction, health score
- **Health Precautions**: AI-recommended health advice based on real climate data

## Tech Stack

- **Frontend**: React.js, Mapbox GL JS, CSS Modules
- **Backend**: FastAPI, Python
- **Database**: MongoDB
- **ML Models**: scikit-learn (K-Means), XGBoost
- **Data**: Real-time Pune temperature data

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file with your Mapbox token:
```
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=http://localhost:8000
```

4. Run the frontend:
```bash
npm start
```

## API Endpoints

- `GET /api/v1/heatmap_data` - Get thermal heatmap data for Pune
- `POST /api/v1/simulate_intervention` - Simulate intervention impact
- `GET /api/v1/recommendations` - Get AI recommendations
- `GET /api/v1/health_precautions` - Get health precautions based on climate data

## ML Models

- **K-Means Clustering**: Identifies distinct UHI hotspot zones
- **XGBoost Regression**: Predicts temperature reduction and impact metrics

## License

MIT


