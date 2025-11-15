# Setup Instructions

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- MongoDB (optional, for production)
- Mapbox account (free tier is sufficient)

## Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory:
```bash
cp .env.example .env
```

6. Edit `.env` file with your configuration:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=uhi_db
OPENWEATHER_API_KEY=your_openweather_api_key_here  # Optional, for real-time data
API_HOST=0.0.0.0
API_PORT=8000
```

7. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```bash
cp .env.example .env
```

4. Edit `.env` file with your Mapbox token:
```
REACT_APP_MAPBOX_TOKEN=your_mapbox_token_here
REACT_APP_API_URL=http://localhost:8000
```

5. Get a Mapbox token:
   - Go to https://account.mapbox.com/
   - Sign up for a free account
   - Copy your access token
   - Paste it in the `.env` file

6. Run the frontend:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Getting a Mapbox Token

1. Visit https://account.mapbox.com/
2. Sign up for a free account
3. Go to your account page
4. Copy your default public token
5. Paste it in `frontend/.env` as `REACT_APP_MAPBOX_TOKEN`

## Getting an OpenWeatherMap API Key (Optional)

The application works without this, but for real-time weather data:

1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to `backend/.env` as `OPENWEATHER_API_KEY`

## Testing the Application

1. Start the backend server (port 8000)
2. Start the frontend (port 3000)
3. Open http://localhost:3000 in your browser
4. You should see the UHI Mitigation System dashboard
5. Click on the map tools to add interventions
6. Click "Simulate" to see the impact

## Troubleshooting

### Backend Issues

- **Port already in use**: Change the port in `backend/.env` or stop the process using port 8000
- **Import errors**: Make sure you're in the virtual environment and all dependencies are installed
- **CORS errors**: Check that the frontend URL is in the CORS origins list in `backend/app/main.py`

### Frontend Issues

- **Map not loading**: Check that your Mapbox token is correct in `.env`
- **API errors**: Make sure the backend is running on port 8000
- **Module not found**: Run `npm install` again

### Mapbox Issues

- **Token errors**: Verify your token is correct and has the right permissions
- **Style errors**: The default style should work, but you can change it in `MapContainer.js`

## Project Structure

```
UHI/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── models/           # ML models
│   │   ├── routes/           # API routes
│   │   ├── services/         # Business logic
│   │   └── utils/            # Utility functions
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── contexts/         # React contexts
│   │   ├── services/         # API services
│   │   └── App.js
│   ├── package.json
│   └── .env
└── README.md
```

## API Endpoints

- `GET /api/v1/heatmap_data` - Get thermal heatmap data for Pune
- `POST /api/v1/simulate_intervention` - Simulate intervention impact
- `GET /api/v1/recommendations` - Get AI recommendations
- `GET /api/v1/health_precautions` - Get health precautions

## Features

- Interactive thermal heatmap of Pune
- Add interventions (trees, cool roofs, parks, green roofs)
- Real-time impact simulation
- AI-generated recommendations
- Health precautions based on climate data
- Dark/Light mode toggle


