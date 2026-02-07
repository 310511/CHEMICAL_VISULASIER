import React from 'react';

const HistoryList = ({ history, onDatasetSelect, selectedDatasetId }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const handleRowClick = (datasetId) => {
    if (onDatasetSelect) {
      onDatasetSelect(datasetId);
    }
  };

  if (history.length === 0) {
    return (
      <div className="card">
        <p style={{ 
          textAlign: 'center', 
          color: '#666', 
          fontStyle: 'italic',
          padding: '20px'
        }}>
          No upload history available.
        </p>
      </div>
    );
  }

  return (
    <div className="card">
      <div style={{ overflowX: 'auto' }}>
        <table className="table">
          <thead>
            <tr>
              <th>Filename</th>
              <th>Upload Date</th>
              <th>Equipment Count</th>
              <th>Avg Flowrate</th>
              <th>Avg Pressure</th>
              <th>Avg Temperature</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr 
                key={item.id}
                style={{
                  backgroundColor: selectedDatasetId === item.id ? '#e6f3ff' : 'transparent',
                  cursor: 'pointer'
                }}
                onClick={() => handleRowClick(item.id)}
              >
                <td>
                  <span style={{ fontWeight: '500' }}>
                    {item.filename}
                  </span>
                  {selectedDatasetId === item.id && (
                    <span style={{ 
                      marginLeft: '10px', 
                      color: '#007bff',
                      fontSize: '12px',
                      fontWeight: 'bold'
                    }}>
                      (Current)
                    </span>
                  )}
                </td>
                <td>{formatDate(item.upload_timestamp)}</td>
                <td>
                  <span style={{
                    backgroundColor: '#007bff',
                    color: 'white',
                    padding: '2px 8px',
                    borderRadius: '12px',
                    fontSize: '12px'
                  }}>
                    {item.total_count}
                  </span>
                </td>
                <td>{item.avg_flowrate.toFixed(2)} L/min</td>
                <td>{item.avg_pressure.toFixed(2)} bar</td>
                <td>{item.avg_temperature.toFixed(2)} °C</td>
                <td>
                  <button
                    className="btn btn-primary"
                    style={{ fontSize: '12px', padding: '4px 8px' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRowClick(item.id);
                    }}
                  >
                    Load Dataset
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div style={{ 
        marginTop: '15px', 
        fontSize: '14px', 
        color: '#666',
        fontStyle: 'italic'
      }}>
        <small>
          Note: Only the last 5 uploads are retained. Click on any row to load that dataset.
        </small>
      </div>
    </div>
  );
};

export default HistoryList;
