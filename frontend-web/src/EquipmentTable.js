import React, { useState } from 'react';

const EquipmentTable = ({ equipment }) => {
  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: 'ascending'
  });

  const handleSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedEquipment = React.useMemo(() => {
    let sortableEquipment = [...equipment];
    if (sortConfig.key !== null) {
      sortableEquipment.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableEquipment;
  }, [equipment, sortConfig]);

  const getSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) {
      return '↕️';
    }
    return sortConfig.direction === 'ascending' ? '↑' : '↓';
  };

  return (
    <div className="card">
      <h3 style={{ marginBottom: '20px', color: '#333' }}>
        Equipment List ({equipment.length} items)
      </h3>
      
      <div style={{ overflowX: 'auto' }}>
        <table className="table">
          <thead>
            <tr>
              <th 
                onClick={() => handleSort('equipment_name')}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                Equipment Name {getSortIcon('equipment_name')}
              </th>
              <th 
                onClick={() => handleSort('type')}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                Type {getSortIcon('type')}
              </th>
              <th 
                onClick={() => handleSort('flowrate')}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                Flowrate (L/min) {getSortIcon('flowrate')}
              </th>
              <th 
                onClick={() => handleSort('pressure')}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                Pressure (bar) {getSortIcon('pressure')}
              </th>
              <th 
                onClick={() => handleSort('temperature')}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                Temperature (°C) {getSortIcon('temperature')}
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedEquipment.map((item, index) => (
              <tr key={item.id}>
                <td>{item.equipment_name}</td>
                <td>
                  <span 
                    style={{
                      backgroundColor: getTypeColor(item.type),
                      color: 'white',
                      padding: '2px 8px',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: '500'
                    }}
                  >
                    {item.type}
                  </span>
                </td>
                <td>{item.flowrate.toFixed(1)}</td>
                <td>{item.pressure.toFixed(1)}</td>
                <td>{item.temperature.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {equipment.length === 0 && (
        <div style={{ 
          textAlign: 'center', 
          padding: '40px', 
          color: '#666',
          fontStyle: 'italic'
        }}>
          No equipment data available. Please upload a CSV file to get started.
        </div>
      )}
    </div>
  );
};

const getTypeColor = (type) => {
  const colors = {
    'Reactor': '#007bff',
    'Pump': '#28a745',
    'Heat Exchanger': '#ffc107',
    'Compressor': '#dc3545',
    'Valve': '#6c757d'
  };
  return colors[type] || '#6c757d';
};

export default EquipmentTable;
