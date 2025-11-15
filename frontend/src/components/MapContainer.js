import React, { useState, useEffect, useRef } from 'react';
import Map, { Source, Layer, Marker } from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { FaTree, FaHome, FaCampground, FaLayerGroup, FaTrash, FaRedo, FaPlay } from 'react-icons/fa';
import { getHeatmapData, simulateIntervention } from '../services/api';
import './MapContainer.css';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN || 'pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

const MapContainer = ({ onInterventionAdd, onSimulation, interventions, onInterventionRemove }) => {
  const [viewport, setViewport] = useState({
    latitude: 18.5204,
    longitude: 73.8567,
    zoom: 12
  });
  const [heatmapData, setHeatmapData] = useState(null);
  const [selectedTool, setSelectedTool] = useState(null);
  const [tempMarkers, setTempMarkers] = useState([]);
  const mapRef = useRef(null);

  useEffect(() => {
    fetchHeatmapData();
  }, []);

  // Update baseline when heatmap data changes
  useEffect(() => {
    if (heatmapData?.metadata?.avg_temperature) {
      setBaselineTemperature(heatmapData.metadata.avg_temperature);
    }
  }, [heatmapData]);

  useEffect(() => {
    // Update markers when interventions change
    const markers = interventions.map(intervention => ({
      id: intervention.id,
      lat: intervention.location[0],
      lng: intervention.location[1],
      type: intervention.type
    }));
    setTempMarkers(markers);
  }, [interventions]);

  const [baselineTemperature, setBaselineTemperature] = useState(38.5);

  const fetchHeatmapData = async () => {
    try {
      const data = await getHeatmapData();
      setHeatmapData(data);
      // Store baseline temperature for comparison, but don't overwrite simulation results
      if (data.metadata && data.metadata.avg_temperature) {
        const baseline = data.metadata.avg_temperature;
        setBaselineTemperature(baseline);
        // Only set initial metrics if no interventions have been simulated yet
        if (interventions.length === 0) {
          onSimulation({
            average_temperature: baseline,
            temperature_reduction: 0,
            energy_saving: 0,
            co2_reduction: 0,
            health_score: 7.2
          });
        }
      }
    } catch (error) {
      console.error('Error fetching heatmap data:', error);
      // Set fallback data if API fails
      setHeatmapData({
        type: "FeatureCollection",
        features: [],
        metadata: { city: "Pune", avg_temperature: 35 }
      });
    }
  };

  const [simulating, setSimulating] = useState(false);

  const simulateInterventions = async () => {
    if (interventions.length === 0) {
      alert('Please add at least one intervention before simulating.');
      return;
    }
    
    setSimulating(true);
    try {
      const simulationData = interventions.map(intervention => ({
        type: intervention.type,
        count: intervention.count || 0,
        area: intervention.area || 0,
        location: intervention.location,
        base_temperature: intervention.base_temperature || baselineTemperature
      }));

      const data = await simulateIntervention(simulationData);
      
      // Use the data directly from backend (it already calculates city-wide reduction)
      const formattedData = {
        average_temperature: data.average_temperature || baselineTemperature,
        temperature_reduction: data.temperature_reduction || 0,
        energy_saving: data.energy_saving || 0,
        co2_reduction: data.co2_reduction || 0,
        health_score: data.health_score || 7.2
      };
      
      onSimulation(formattedData);
      console.log('Simulation completed:', formattedData);
    } catch (error) {
      console.error('Error simulating interventions:', error);
      alert(`Failed to simulate interventions: ${error.message || 'Please ensure the backend server is running.'}`);
    } finally {
      setSimulating(false);
    }
  };

  const handleMapClick = (e) => {
    if (!selectedTool) return;

    const { lng, lat } = e.lngLat;
    const interventionId = Date.now();
    const intervention = {
      id: interventionId,
      type: selectedTool,
      location: [lat, lng],
      count: selectedTool === 'trees' ? 20 : 0,
      area: selectedTool !== 'trees' ? 500 : 0,
      base_temperature: 35
    };

    onInterventionAdd(intervention);
    setTempMarkers(prev => [...prev, { id: interventionId, lat, lng, type: selectedTool }]);
    setSelectedTool(null);
  };

  const getInterventionIcon = (type) => {
    switch (type) {
      case 'trees':
        return <FaTree />;
      case 'cool_roof':
        return <FaHome />;
      case 'park':
        return <FaCampground />;
      case 'green_roof':
        return <FaLayerGroup />;
      default:
        return <FaTree />;
    }
  };

  const getInterventionColor = (type) => {
    switch (type) {
      case 'trees':
        return '#10b981';
      case 'cool_roof':
        return '#3b82f6';
      case 'park':
        return '#22c55e';
      case 'green_roof':
        return '#84cc16';
      default:
        return '#10b981';
    }
  };

  const heatmapLayer = {
    id: 'heatmap',
    type: 'heatmap',
    paint: {
      'heatmap-weight': {
        property: 'temperature',
        type: 'exponential',
        stops: [[0, 0], [30, 1], [40, 2]]
      },
      'heatmap-intensity': {
        stops: [[0, 0.5], [12, 1]]
      },
      'heatmap-color': [
        'interpolate',
        ['linear'],
        ['heatmap-density'],
        0, 'rgba(33,102,172,0)',
        0.2, 'rgb(103,169,207)',
        0.4, 'rgb(209,229,240)',
        0.6, 'rgb(253,219,199)',
        0.8, 'rgb(239,138,98)',
        1, 'rgb(178,24,43)'
      ],
      'heatmap-radius': {
        stops: [[0, 2], [12, 20]]
      },
      'heatmap-opacity': {
        default: 1,
        stops: [[0, 0.6], [12, 0.8]]
      }
    }
  };

  const handleReset = () => {
    setViewport({
      latitude: 18.5204,
      longitude: 73.8567,
      zoom: 12
    });
    if (mapRef.current) {
      mapRef.current.flyTo({
        center: [73.8567, 18.5204],
        zoom: 12,
        duration: 1000
      });
    }
  };

  return (
    <div className="map-container">
      <div className="map-header">
        <h2 className="map-title">Thermal Heat Map - Pune, India</h2>
        <div className="map-header-actions">
          <button className="header-button reset" onClick={handleReset} title="Reset Map">
            <FaRedo /> Reset
          </button>
          <button 
            className="header-button simulate" 
            onClick={simulateInterventions}
            disabled={simulating || interventions.length === 0}
            title="Run Simulation"
          >
            <FaPlay /> Run Simulation ({interventions.length})
          </button>
        </div>
      </div>
      <div className="map-wrapper">
        <div className="map-controls-left">
          <button
            className={`map-control-button ${selectedTool === 'trees' ? 'active' : ''}`}
            onClick={() => setSelectedTool('trees')}
            title="Add Trees"
          >
            <FaTree />
            <span>Add Trees</span>
          </button>
          <button
            className={`map-control-button ${selectedTool === 'cool_roof' ? 'active' : ''}`}
            onClick={() => setSelectedTool('cool_roof')}
            title="Cool Roof"
          >
            <FaHome />
            <span>Cool Roof</span>
          </button>
          <button
            className={`map-control-button ${selectedTool === 'park' ? 'active' : ''}`}
            onClick={() => setSelectedTool('park')}
            title="New Park"
          >
            <FaCampground />
            <span>New Park</span>
          </button>
        </div>
        <Map
          ref={mapRef}
          initialViewState={viewport}
          mapboxAccessToken={MAPBOX_TOKEN}
          style={{ width: '100%', height: '100%' }}
          mapStyle="mapbox://styles/mapbox/streets-v11"
          onMove={evt => setViewport(evt.viewState)}
          onClick={handleMapClick}
        >
          {heatmapData && (
            <Source
              id="heatmap-data"
              type="geojson"
              data={heatmapData}
            >
              <Layer {...heatmapLayer} />
            </Source>
          )}
          {tempMarkers.map(marker => (
            <Marker
              key={marker.id}
              latitude={marker.lat}
              longitude={marker.lng}
            >
              <div
                className="intervention-marker"
                style={{ color: getInterventionColor(marker.type) }}
              >
                {getInterventionIcon(marker.type)}
              </div>
            </Marker>
          ))}
        </Map>
        <div className="temperature-scale">
          <div className="scale-label">Temperature Scale</div>
          <div className="scale-gradient">
            <span className="scale-min">30°C</span>
            <div className="scale-bar"></div>
            <span className="scale-max">50°C</span>
          </div>
        </div>
      </div>
      <div className="interventions-list">
        <h4>Added Interventions ({interventions.length})</h4>
        {interventions.map((intervention, index) => (
          <div key={intervention.id || index} className="intervention-item">
            <span>{getInterventionIcon(intervention.type)} {intervention.type}</span>
            <button onClick={() => onInterventionRemove(index)}>
              <FaTrash />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MapContainer;

