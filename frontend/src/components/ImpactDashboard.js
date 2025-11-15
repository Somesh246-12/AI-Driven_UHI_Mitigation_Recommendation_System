import React from 'react';
import StatCard from './StatCard';
import './ImpactDashboard.css';

const ImpactDashboard = ({ metrics, previousMetrics }) => {
  const safeValue = (value, defaultValue = 0) => {
    return value !== undefined && value !== null && !isNaN(value) ? value : defaultValue;
  };

  const avgTemp = safeValue(metrics.average_temperature, 38.5);
  const tempReduction = safeValue(metrics.temperature_reduction, 0);
  const energySaving = safeValue(metrics.energy_saving, 0);
  const co2Reduction = safeValue(metrics.co2_reduction, 0);
  const healthScore = safeValue(metrics.health_score, 7.2);

  // Calculate changes vs last simulation
  const getTempChange = () => {
    if (!previousMetrics) return 'No change';
    const prev = safeValue(previousMetrics.average_temperature, 38.5);
    const change = prev - avgTemp;
    if (change > 0) return `-${change.toFixed(1)}°C vs last simulation`;
    if (change < 0) return `+${Math.abs(change).toFixed(1)}°C vs last simulation`;
    return 'No change';
  };

  const getEnergyChange = () => {
    if (!previousMetrics) return 'vs baseline';
    const prev = safeValue(previousMetrics.energy_saving, 0);
    const change = energySaving - prev;
    if (change > 0) return `+${change.toFixed(1)} MWh vs last simulation`;
    if (change < 0) return `${change.toFixed(1)} MWh vs last simulation`;
    return 'vs last simulation';
  };

  const getCO2Change = () => {
    if (!previousMetrics) return 'Estimated';
    const prev = safeValue(previousMetrics.co2_reduction, 0);
    const change = co2Reduction - prev;
    if (change > 0) return `+${change.toFixed(0)} kg vs last simulation`;
    if (change < 0) return `${change.toFixed(0)} kg vs last simulation`;
    return 'vs last simulation';
  };

  const getHealthChange = () => {
    if (!previousMetrics) return 'Health index';
    const prev = safeValue(previousMetrics.health_score, 7.2);
    const change = healthScore - prev;
    if (change > 0) return `+${change.toFixed(1)} vs last simulation`;
    if (change < 0) return `${change.toFixed(1)} vs last simulation`;
    return 'vs last simulation';
  };

  return (
    <div className="impact-dashboard">
      <StatCard
        title="Average Temperature"
        value={`${avgTemp.toFixed(1)}°C`}
        change={getTempChange()}
        trend={tempReduction > 0 ? 'up' : 'neutral'}
        icon="🌡️"
      />
      <StatCard
        title="Potential Energy Saving"
        value={`${energySaving.toFixed(1)} MWh`}
        change={getEnergyChange()}
        trend={energySaving > 0 ? 'up' : 'neutral'}
        icon="⚡"
      />
      <StatCard
        title="CO2 Reduction"
        value={`${co2Reduction.toFixed(0)} kg`}
        change={getCO2Change()}
        trend={co2Reduction > 0 ? 'up' : 'neutral'}
        icon="🌱"
      />
      <StatCard
        title="Public Health Score"
        value={`${healthScore.toFixed(1)}/10`}
        change={getHealthChange()}
        trend={healthScore > 7 ? 'up' : 'neutral'}
        icon="❤️"
      />
    </div>
  );
};

export default ImpactDashboard;

