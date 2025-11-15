import React from 'react';
import { FaArrowUp, FaArrowDown, FaEllipsisV } from 'react-icons/fa';
import './StatCard.css';

const StatCard = ({ title, value, change, trend, icon }) => {
  const isPositive = trend === 'up';
  const isNegative = trend === 'down';

  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <h3 className="stat-card-title">{title}</h3>
        <button className="stat-card-menu">
          <FaEllipsisV />
        </button>
      </div>
      <div className="stat-card-content">
        <div className="stat-card-icon">{icon}</div>
        <div className="stat-card-value">{value}</div>
      </div>
      <div className="stat-card-footer">
        <span className={`stat-card-change ${isPositive ? 'positive' : isNegative ? 'negative' : 'neutral'}`}>
          {isPositive && <FaArrowUp />}
          {isNegative && <FaArrowDown />}
          {change}
        </span>
      </div>
    </div>
  );
};

export default StatCard;


