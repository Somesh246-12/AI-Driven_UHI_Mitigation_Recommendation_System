import React from 'react';
import './Analytics.css';

const Analytics = () => {
  const impactCards = [
    { label: 'Avg City Temp', value: '34.2°C', change: '-0.8°C vs last week' },
    { label: 'Projected CO₂ Reduction', value: '22.4 kt', change: '+4.1 kt with new plans' },
    { label: 'Energy Savings', value: '18.6 GWh', change: '+6% from baseline' },
    { label: 'Public Health Index', value: '8.4 / 10', change: '+0.6 vs last season' }
  ];

  const temperatureTrend = [
    { day: 'Mon', value: 36.5 },
    { day: 'Tue', value: 36.1 },
    { day: 'Wed', value: 35.8 },
    { day: 'Thu', value: 35.3 },
    { day: 'Fri', value: 34.9 },
    { day: 'Sat', value: 34.4 },
    { day: 'Sun', value: 34.2 }
  ];

  const adoptionRates = [
    { label: 'Cool Roof Retrofits', value: 72 },
    { label: 'Urban Tree Cover', value: 58 },
    { label: 'Green Corridors', value: 43 },
    { label: 'Water Features', value: 38 }
  ];

  const riskHotspots = [
    { label: 'Central Business District', severity: 'high', value: 39.4 },
    { label: 'Industrial Belt', severity: 'medium', value: 37.2 },
    { label: 'Riverside Ward', severity: 'low', value: 34.1 }
  ];

  return (
    <div className="analytics-page">
      <section className="analytics-section">
        <div className="section-header">
          <h2>Citywide Impact Overview</h2>
          <p>Live modeling of mitigation strategies across Pune</p>
        </div>
        <div className="analytics-cards">
          {impactCards.map((card) => (
            <div className="analytics-card" key={card.label}>
              <p className="card-label">{card.label}</p>
              <p className="card-value">{card.value}</p>
              <span className="card-change">{card.change}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="analytics-section split">
        <div className="chart-card">
          <div className="section-header">
            <h3>Temperature Trend (7 Day)</h3>
            <span className="badge cool">Cooling</span>
          </div>
          <div className="line-chart">
            {temperatureTrend.map((point) => (
              <div className="line-point" key={point.day}>
                <div className="point-value">{point.value.toFixed(1)}°</div>
                <div
                  className="point-bar"
                  style={{
                    height: `${point.value * 2}px`
                  }}
                />
                <span className="point-label">{point.day}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="chart-card">
          <div className="section-header">
            <h3>Mitigation Adoption</h3>
            <span className="badge warm">In Progress</span>
          </div>
          <div className="bar-chart">
            {adoptionRates.map((item) => (
              <div className="bar-row" key={item.label}>
                <span className="bar-label">{item.label}</span>
                <div className="bar-track">
                  <div
                    className="bar-fill"
                    style={{ width: `${item.value}%` }}
                  />
                </div>
                <span className="bar-value">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="analytics-section">
        <div className="section-header">
          <h3>Heat Risk Hotspots</h3>
          <p>Priority neighborhoods requiring immediate intervention</p>
        </div>
        <div className="hotspot-list">
          {riskHotspots.map((spot) => (
            <div className={`hotspot-card ${spot.severity}`} key={spot.label}>
              <div>
                <p className="hotspot-label">{spot.label}</p>
                <span className="hotspot-temperature">{spot.value.toFixed(1)}°C</span>
              </div>
              <span className="severity-tag">{spot.severity.toUpperCase()}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Analytics;


