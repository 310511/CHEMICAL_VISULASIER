import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authAPI, equipmentAPI } from './api';
import UploadForm from './UploadForm';
import SummaryCards from './SummaryCards';
import ChartsSection from './ChartsSection';
import EquipmentTable from './EquipmentTable';
import HistoryList from './HistoryList';

const Dashboard = () => {
  const [summary, setSummary] = useState(null);
  const [equipment, setEquipment] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedDatasetId, setSelectedDatasetId] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const fetchInitialData = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const [summaryRes, equipmentRes, historyRes] = await Promise.all([
        equipmentAPI.getSummary(),
        equipmentAPI.getEquipment(),
        equipmentAPI.getHistory()
      ]);

      setSummary(summaryRes.data);
      setEquipment(equipmentRes.data);
      setHistory(historyRes.data);
    } catch (err) {
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleUploadSuccess = useCallback(async (datasetId) => {
    setUploadProgress(0);
    try {
      const [summaryRes, equipmentRes, historyRes] = await Promise.all([
        equipmentAPI.getSummary(datasetId),
        equipmentAPI.getEquipment(datasetId),
        equipmentAPI.getHistory()
      ]);

      setSummary(summaryRes.data);
      setEquipment(equipmentRes.data);
      setHistory(historyRes.data);
      setSelectedDatasetId(datasetId);
    } catch (err) {
      setError('Failed to refresh data after upload.');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDownloadPDF = useCallback(async () => {
    if (!summary || summary.total_count === 0) {
      setError('No data available to generate report.');
      return;
    }

    try {
      setError('');
      const response = await equipmentAPI.downloadPDF(selectedDatasetId);
      const url = window.URL.createObjectURL(new Blob([response.data]), {
        type: 'application/pdf'
      });
      const link = document.createElement('a');
      link.href = url;
      link.download = `equipment_report_${selectedDatasetId || 'latest'}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      setError('PDF report downloaded successfully!');
    } catch (err) {
      setError('Failed to download PDF report.');
    }
  }, [summary, selectedDatasetId]);

  const handleLogout = useCallback(async () => {
    try {
      await authAPI.logout();
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      navigate('/login');
    } catch (err) {
      setError('Failed to logout. Please try again.');
    }
  }, [navigate]);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  return (
    <div>
      {/* Enhanced Navigation Bar */}
      <nav className="navbar">
        <div className="navbar-brand">
          <span>⚗️</span>
          Chemical Equipment Visualizer
          <span style={{ 
            fontSize: '0.8rem', 
            opacity: 0.8, 
            marginLeft: '8px' 
          }}>
            v2.0
          </span>
        </div>
        <div className="navbar-nav">
          <button 
            className="btn btn-secondary" 
            onClick={handleLogout}
            style={{ 
              background: 'rgba(220, 53, 69, 0.3)', 
              border: '1px solid rgba(220, 53, 69, 0.5)',
              fontSize: '12px'
            }}
          >
            🚪 Logout
          </button>
        </div>
      </nav>

      <div className="container">
        {error && (
          <div className="alert alert-error" style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <span>{error}</span>
            <button 
              onClick={() => setError('')}
              style={{ 
                background: 'none', 
                border: 'none', 
                color: 'white', 
                cursor: 'pointer',
                fontSize: '16px',
                padding: '4px 8px',
                borderRadius: '4px'
              }}
            >
              ×
            </button>
          </div>
        )}

        {/* Upload Section with Progress */}
        <UploadForm 
          onUploadSuccess={handleUploadSuccess}
          uploadProgress={uploadProgress}
          setUploadProgress={setUploadProgress}
        />

        {/* Summary Statistics */}
        {summary && <SummaryCards summary={summary} />}

        {/* Charts Section */}
        {summary && <ChartsSection summary={summary} />}

        {/* Actions Bar */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '20px',
          padding: '16px',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '12px',
          border: '1px solid rgba(0, 0, 0, 0.1)'
        }}>
          <h3 style={{ 
            margin: '0', 
            color: '#2c3e50',
            fontSize: '1.2rem',
            fontWeight: '600'
          }}>
            📊 Equipment Data Analysis
          </h3>
          <button 
            className="btn btn-success"
            onClick={handleDownloadPDF}
            disabled={!summary || summary.total_count === 0}
            style={{ 
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
          >
            <span>📄</span>
            Download PDF Report
          </button>
        </div>

        {/* Equipment Table */}
        {equipment.length > 0 && <EquipmentTable equipment={equipment} />}

        {/* History Section */}
        <div style={{ marginTop: '40px' }}>
          <h3 style={{ 
            marginBottom: '20px',
            color: '#2c3e50',
            fontSize: '1.2rem',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            <span>📚</span>
            Upload History & Dataset Management
          </h3>
          <HistoryList 
            history={history} 
            onDatasetSelect={handleUploadSuccess}
            selectedDatasetId={selectedDatasetId}
          />
        </div>

        {/* Status Bar */}
        <div style={{
          position: 'fixed',
          bottom: '0',
          left: '0',
          right: '0',
          background: 'linear-gradient(135deg, #2c3e50, #343a40)',
          color: 'white',
          padding: '12px 24px',
          fontSize: '14px',
          boxShadow: '0 -4px 6px rgba(0, 0, 0, 0.3)',
          zIndex: '1000',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {loading && <span style={{ 
              width: '12px', 
              height: '12px', 
              border: '2px solid rgba(255, 255, 255, 0.3)', 
              borderRadius: '50%', 
              borderTop: '2px solid transparent',
              animation: 'spin 1s linear infinite' 
            }}></span>}
            <span style={{ fontSize: '12px', fontWeight: '500' }}>
              {loading ? 'Processing data...' : `Ready • ${equipment.length} items loaded`}
            </span>
          </div>
          <div style={{ fontSize: '12px', opacity: '0.7' }}>
            {selectedDatasetId ? `Dataset ${selectedDatasetId} selected` : 'Latest dataset'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
