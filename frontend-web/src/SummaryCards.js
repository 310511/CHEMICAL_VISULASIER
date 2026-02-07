import React from 'react';

const SummaryCards = ({ summary }) => {
  const cards = [
    {
      title: 'Total Equipment',
      value: summary.total_count,
      unit: 'items',
      color: '#007bff'
    },
    {
      title: 'Average Flowrate',
      value: summary.avg_flowrate.toFixed(2),
      unit: 'L/min',
      color: '#28a745'
    },
    {
      title: 'Average Pressure',
      value: summary.avg_pressure.toFixed(2),
      unit: 'bar',
      color: '#ffc107'
    },
    {
      title: 'Average Temperature',
      value: summary.avg_temperature.toFixed(2),
      unit: '°C',
      color: '#dc3545'
    }
  ];

  return (
    <div className="stats-grid">
      {cards.map((card, index) => (
        <div 
          key={index}
          className="stat-card"
          style={{ 
            background: `linear-gradient(135deg, ${card.color} 0%, ${card.color}dd 100%)`
          }}
        >
          <h3>{card.value}</h3>
          <p>{card.title}</p>
          <small style={{ opacity: 0.8 }}>{card.unit}</small>
        </div>
      ))}
    </div>
  );
};

export default SummaryCards;
