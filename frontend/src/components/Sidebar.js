import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaHome, FaChartBar } from 'react-icons/fa';
import './Sidebar.css';

const navItems = [
  { path: '/', label: 'Dashboard', icon: <FaHome /> },
  { path: '/analytics', label: 'Analytics', icon: <FaChartBar /> }
];

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-square">
          <span>U</span>
        </div>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            title={item.label}
          >
            <span className="nav-icon">{item.icon}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;


