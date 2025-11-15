import React, { useState, useEffect } from 'react';
import { 
  FaExclamationTriangle, 
  FaInfoCircle, 
  FaCheckCircle,
  FaSun,
  FaWind,
  FaTint
} from 'react-icons/fa';
import { getHealthPrecautions } from '../services/api';
import './HealthPrecautions.css';

const HealthPrecautions = () => {
  const [precautions, setPrecautions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Detect dark mode changes
  useEffect(() => {
    const checkDarkMode = () => {
      setIsDarkMode(document.documentElement.classList.contains('dark'));
    };
    
    checkDarkMode();
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });
    
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    fetchHealthPrecautions(true);
    // Auto-refresh health precautions every 90 seconds to get real-time weather updates (reduced frequency)
    const interval = setInterval(() => {
      fetchHealthPrecautions(false); // Don't show loading on refresh
    }, 90000); // 90 seconds
    
    return () => clearInterval(interval);
  }, []);

  const fetchHealthPrecautions = async (showLoading = true) => {
    try {
      if (showLoading) {
        setLoading(true);
        setError(null);
      }
      const data = await getHealthPrecautions();
      if (data && Array.isArray(data)) {
        setPrecautions(data);
        setError(null);
      } else {
        console.warn('Invalid health precautions data received');
        setPrecautions([]);
      }
    } catch (error) {
      console.error('Error fetching health precautions:', error);
      // Only show error on initial load
      if (showLoading) {
        setPrecautions([]);
        // Show user-friendly error message
        if (error.message?.includes('Network') || error.code === 'ECONNREFUSED' || error.message?.includes('Failed to fetch')) {
          setError('Backend server is not running. Please start the backend server at http://localhost:8000');
        } else {
          setError('Failed to load health precautions. Please try again later.');
        }
      }
      // If we have existing data and refresh fails, keep showing it silently
    } finally {
      if (showLoading) {
        setLoading(false);
      }
    }
  };

  const getIconForType = (title) => {
    const titleLower = title.toLowerCase();
    if (titleLower.includes('heat') || titleLower.includes('temperature')) {
      return <FaSun className="health-icon" />;
    } else if (titleLower.includes('air') || titleLower.includes('quality')) {
      return <FaWind className="health-icon" />;
    } else if (titleLower.includes('humidity') || titleLower.includes('moisture')) {
      return <FaTint className="health-icon" />;
    } else if (titleLower.includes('uv') || titleLower.includes('radiation')) {
      return <FaExclamationTriangle className="health-icon" />;
    }
    return <FaInfoCircle className="health-icon" />;
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return '#ef4444';
      case 'medium':
        return '#6b7280';
      case 'low':
        return '#10b981';
      default:
        return '#6b7280';
    }
  };

  const getIconBackgroundColor = (severity) => {
    if (isDarkMode) {
      switch (severity) {
        case 'high':
          return 'rgba(239, 68, 68, 0.2)'; // dark mode light red
        case 'medium':
          return 'rgba(245, 158, 11, 0.2)'; // dark mode light orange
        case 'low':
          return 'rgba(16, 185, 129, 0.2)'; // dark mode light green
        default:
          return 'rgba(107, 114, 128, 0.2)'; // dark mode light gray
      }
    } else {
      switch (severity) {
        case 'high':
          return '#fee2e2'; // light red
        case 'medium':
          return '#fed7aa'; // light orange
        case 'low':
          return '#d1fae5'; // light green
        default:
          return '#f3f4f6'; // light gray
      }
    }
  };

  const getIconColor = (severity) => {
    switch (severity) {
      case 'high':
        return '#ef4444'; // red
      case 'medium':
        return '#f59e0b'; // orange
      case 'low':
        return '#10b981'; // green
      default:
        return '#6b7280'; // gray
    }
  };

  if (loading) {
    return (
      <div className="health-precautions">
        <div className="health-header">
          <h2>AI-Recommended Health Precautions</h2>
        </div>
        <div className="health-loading">Loading health precautions...</div>
      </div>
    );
  }

  const activeAlerts = precautions.filter(p => p.severity === 'high').length;

  return (
    <div className="health-precautions">
      <div className="health-header">
        <h2>AI-Recommended Health Precautions</h2>
        {activeAlerts > 0 && (
          <span className="active-alerts">Active Alerts: {activeAlerts}</span>
        )}
      </div>
      <div className="health-content">
        {error ? (
          <div className="health-error">
            <p>⚠️ {error}</p>
            <p>Make sure the backend is running: <code>cd backend && uvicorn app.main:app --reload</code></p>
          </div>
        ) : precautions.length === 0 ? (
          <div className="health-empty">No health precautions available</div>
        ) : (
          <div className="health-items">
            {precautions.map((precaution) => (
              <div
                key={precaution.id}
                className="health-item"
              >
                <div className="health-item-header">
                  <div 
                    className="health-item-icon-wrapper"
                    style={{ 
                      backgroundColor: getIconBackgroundColor(precaution.severity)
                    }}
                  >
                    <div 
                      className="health-item-icon"
                      style={{ color: getIconColor(precaution.severity) }}
                    >
                      {getIconForType(precaution.title)}
                    </div>
                  </div>
                  <div className="health-item-content">
                    <div className="health-item-title-section">
                      <h3>{precaution.title}</h3>
                      <p className="health-item-message">{precaution.message}</p>
                    </div>
                  </div>
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: getSeverityColor(precaution.severity) }}
                  >
                    {precaution.severity.toUpperCase()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthPrecautions;

