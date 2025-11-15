import React, { useState } from 'react';
import MapContainer from '../components/MapContainer';
import ImpactDashboard from '../components/ImpactDashboard';
import RecommendationList from '../components/RecommendationList';
import HealthPrecautions from '../components/HealthPrecautions';

const Dashboard = () => {
  const [interventions, setInterventions] = useState([]);
  const [impactMetrics, setImpactMetrics] = useState({
    average_temperature: 38.5,
    temperature_reduction: 0,
    energy_saving: 0,
    co2_reduction: 0,
    health_score: 7.2
  });
  const [previousMetrics, setPreviousMetrics] = useState(null);

  const handleInterventionAdd = (intervention) => {
    setInterventions((prev) => [...prev, intervention]);
  };

  const handleSimulation = (simulationData) => {
    setPreviousMetrics({ ...impactMetrics });
    setImpactMetrics(simulationData);
  };

  const handleInterventionRemove = (index) => {
    setInterventions((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-top">
        <ImpactDashboard metrics={impactMetrics} previousMetrics={previousMetrics} />
      </div>
      <div className="dashboard-middle">
        <div className="dashboard-left">
          <MapContainer
            onInterventionAdd={handleInterventionAdd}
            onSimulation={handleSimulation}
            interventions={interventions}
            onInterventionRemove={handleInterventionRemove}
          />
        </div>
        <div className="dashboard-right">
          <RecommendationList onInterventionAdd={handleInterventionAdd} />
        </div>
      </div>
      <div className="dashboard-bottom">
        <HealthPrecautions />
      </div>
    </div>
  );
};

export default Dashboard;


