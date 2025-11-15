import React, { useState, useEffect } from 'react';
import { FaMapMarkerAlt, FaArrowRight, FaStar } from 'react-icons/fa';
import { getRecommendations } from '../services/api';
import './RecommendationList.css';

const RecommendationList = ({ onInterventionAdd }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isInitialLoad, setIsInitialLoad] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    fetchRecommendations(true);
    // Auto-refresh recommendations every 60 seconds to get real-time updates (reduced frequency to prevent flickering)
    const interval = setInterval(() => {
      fetchRecommendations(false); // Don't show loading on refresh
    }, 60000); // 60 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchRecommendations = async (showLoading = true) => {
    try {
      if (showLoading) {
        setLoading(true);
        setError(null);
      }
      const data = await getRecommendations();
      if (data && Array.isArray(data)) {
        setRecommendations(data);
        setError(null);
        setLastUpdate(new Date());
      } else {
        console.warn('Invalid recommendations data received');
        setRecommendations([]);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Only show error on initial load
      if (showLoading) {
        setRecommendations([]);
        // Show user-friendly error message
        if (error.message?.includes('Network') || error.code === 'ECONNREFUSED' || error.message?.includes('Failed to fetch')) {
          setError('Backend server is not running. Please start the backend server at http://localhost:8000');
        } else {
          setError('Failed to load recommendations. Please try again later.');
        }
      }
      // If we have existing data and refresh fails, keep showing it silently
    } finally {
      if (showLoading) {
        setLoading(false);
        setIsInitialLoad(false);
      }
    }
  };

  const handleApplyRecommendation = (recommendation) => {
    const intervention = {
      id: Date.now(),
      type: recommendation.type,
      location: [recommendation.location.lat, recommendation.location.lon],
      count: recommendation.count || 0,
      area: recommendation.area || 0,
      base_temperature: 35
    };
    onInterventionAdd(intervention);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High':
        return '#ef4444';
      case 'Medium':
        return '#f59e0b';
      case 'Low':
        return '#10b981';
      default:
        return '#6b7280';
    }
  };

  if (loading) {
    return (
      <div className="recommendation-list">
        <div className="recommendation-header">
          <h2>AI Recommendations</h2>
        </div>
        <div className="recommendation-loading">Loading recommendations...</div>
      </div>
    );
  }

  const getTimeAgo = (date) => {
    if (!date) return '';
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return 'Just now';
    if (diffMins === 1) return '1 min ago';
    return `${diffMins} min ago`;
  };

  return (
    <div className="recommendation-list">
      <div className="recommendation-header">
        <div>
          <h2>AI Recommendations</h2>
          {lastUpdate && (
            <span className="update-time">Updated {getTimeAgo(lastUpdate)}</span>
          )}
        </div>
      </div>
      <div className="recommendation-content">
        {error ? (
          <div className="recommendation-error">
            <p style={{ color: '#ef4444', marginBottom: '8px' }}>⚠️ {error}</p>
            <p style={{ fontSize: '12px', color: '#6b7280' }}>Make sure the backend is running: <code>cd backend && uvicorn app.main:app --reload</code></p>
          </div>
        ) : recommendations.length === 0 ? (
          <div className="recommendation-empty">No recommendations available</div>
        ) : (
          <div className="recommendation-items">
            {recommendations.map((recommendation) => (
              <div key={recommendation.id} className="recommendation-item">
                <div className="recommendation-item-header">
                  <h3>{recommendation.action}</h3>
                  <span
                    className="priority-badge"
                    style={{ backgroundColor: getPriorityColor(recommendation.priority) }}
                  >
                    {recommendation.priority}
                  </span>
                </div>
                <p className="recommendation-description">{recommendation.description}</p>
                <div className="recommendation-location">
                  <FaMapMarkerAlt />
                  <span>{recommendation.location.address}</span>
                </div>
                <div className="recommendation-impact">
                  <div className="impact-item">
                    <span className="impact-label">Temp Reduction:</span>
                    <span className="impact-value">
                      -{recommendation.estimated_impact.temp_reduction}°C
                    </span>
                  </div>
                  <div className="impact-item">
                    <span className="impact-label">Cost:</span>
                    <span className="impact-value">{recommendation.estimated_impact.cost}</span>
                  </div>
                </div>
                <button
                  className="recommendation-apply"
                  onClick={() => handleApplyRecommendation(recommendation)}
                >
                  Apply <FaArrowRight />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationList;

