import React from 'react';
import { useLocation } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';
import './Header.css';

const Header = () => {
  const { isDarkMode, toggleTheme } = useTheme();
  const location = useLocation();

  const pageTitles = {
    '/': 'UHI Mitigation Dashboard',
    '/analytics': 'Urban Analytics & Insights'
  };

  const headerTitle = pageTitles[location.pathname] || 'UHI Mitigation System';

  return (
    <div className={`header ${isDarkMode ? 'dark' : ''}`}>
      <div className="header-left">
        <h1 className="header-title">{headerTitle}</h1>
      </div>
      <div className="header-right">
        <label className="theme-toggle">
          <input
            type="checkbox"
            checked={isDarkMode}
            onChange={toggleTheme}
          />
          <span className="slider">
            <span className="slider-label">{isDarkMode ? '🌙' : '☀️'}</span>
          </span>
        </label>
      </div>
    </div>
  );
};

export default Header;


