import React, { useState, useRef, useCallback } from 'react';
import { equipmentAPI } from './api';

const UploadForm = ({ onUploadSuccess, uploadProgress = 0, setUploadProgress }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const validateFile = (selectedFile) => {
    if (!selectedFile) return false;
    
    const fileName = selectedFile.name.toLowerCase();
    const isValidType = selectedFile.type === 'text/csv' || fileName.endsWith('.csv');
    const isValidSize = selectedFile.size <= 10 * 1024 * 1024; // 10MB limit
    
    return isValidType && isValidSize;
  };

  const handleFileSelect = useCallback((selectedFile) => {
    if (validateFile(selectedFile)) {
      setFile(selectedFile);
      setMessage('');
    } else {
      setMessage('Please select a valid CSV file (max 10MB).');
      setFile(null);
    }
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (validateFile(droppedFile)) {
      handleFileSelect(droppedFile);
    } else {
      setMessage('Please select a valid CSV file (max 10MB).');
    }
  }, [validateFile]);

  const simulateProgress = useCallback(() => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15;
      setUploadProgress(Math.min(progress, 90));
      if (progress >= 90) {
        clearInterval(interval);
      }
    }, 100);
    
    return () => {
      clearInterval(interval);
    };
  }, []);

  const handleUpload = useCallback(async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }

    setUploading(true);
    setMessage('');
    setUploadProgress(0);

    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await equipmentAPI.uploadCSV(formData);
      
      if (response.data) {
        setMessage('✅ Upload successful! Processing data...');
        onUploadSuccess(response.data.dataset_id);
        
        // Simulate progress completion
        simulateProgress();
      } else {
        setMessage('❌ Upload failed. Please try again.');
      }
    } catch (error) {
      setMessage(`❌ Upload failed: ${error.response?.data?.error || 'Unknown error'}`);
    } finally {
      setUploading(false);
      setTimeout(() => setUploadProgress(0), 500);
    }
  }, [file, onUploadSuccess, simulateProgress]);

  const getFileIcon = () => {
    if (file) {
      return '📄';
    }
    return '📁';
  };

  const formatFileSize = (bytes) => {
    if (typeof bytes !== 'number') {
      return '';
    }

    if (bytes < 1024) {
      return `${bytes} Bytes`;
    }

    const kb = bytes / 1024;
    if (kb < 1024) {
      return `${kb.toFixed(2)} KB`;
    }

    const mb = kb / 1024;
    return `${mb.toFixed(2)} MB`;
  };

  return (
    <div className="card">
      <h3 style={{
        marginBottom: '24px',
        color: '#2c3e50',
        fontSize: '1.5rem',
        fontWeight: '600',
        display: 'flex',
        alignItems: 'center',
        gap: '12px'
      }}>
        <span>📤</span>
        Smart File Upload
      </h3>

      <div 
        className={`upload-area ${dragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={(e) => handleFileSelect(e.target.files[0])}
          style={{ display: 'none' }}
          disabled={uploading}
        />
        
        <div style={{ textAlign: 'center' }}>
          {file ? (
            <div>
              <div style={{ fontSize: '3rem', color: '#28a745' }}>
                {getFileIcon()} {file.name}
              </div>
              <div style={{ fontSize: '0.9rem', color: '#6c757d', marginBottom: '1rem' }}>
                {formatFileSize(file.size)}
              </div>
            </div>
          ) : (
            <div>
              <div style={{ fontSize: '2.5rem', color: '#6c757d' }}>
                📁 Drag & drop your CSV file here
              </div>
              <div style={{ fontSize: '0.9rem', color: '#17a2b8', marginBottom: '1rem' }}>
                or click to browse
              </div>
              <div style={{ fontSize: '0.8rem', color: '#495057', marginTop: '0.5rem' }}>
                Max file size: 10MB
              </div>
            </div>
          )}
        </div>
      </div>

      {uploading && (
        <div style={{
          marginTop: '20px',
          padding: '16px',
          background: 'rgba(40, 167, 69, 0.1)',
          borderRadius: '8px',
          border: '1px solid rgba(40, 167, 69, 0.3)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            marginBottom: '12px'
          }}>
            <div style={{
              width: '20px',
              height: '20px',
              border: '3px solid rgba(255, 255, 255, 0.3)',
              borderRadius: '50%',
              borderTop: '3px solid transparent',
              animation: 'spin 1s linear infinite'
            }}></div>
            <div style={{ fontSize: '14px', fontWeight: '500' }}>
              Processing and validating your data...
            </div>
          </div>
          
          <div style={{
            background: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '4px',
            height: '8px',
            overflow: 'hidden',
            position: 'relative'
          }}>
            <div style={{
              position: 'absolute',
              top: '0',
              left: '0',
              height: '100%',
              background: 'linear-gradient(90deg, #28a745, #20c997)',
              transition: 'width 0.3s ease',
              width: `${uploadProgress}%`
            }}></div>
          </div>
          
          <div style={{
            fontSize: '12px',
            color: '#495057',
            textAlign: 'center',
            marginTop: '8px'
          }}>
              {uploadProgress}% Complete
            </div>
        </div>
      )}

      {message && (
        <div className={`alert ${message.includes('success') ? 'alert-success' : 'alert-error'}`}>
          {message}
        </div>
      )}

      <div style={{ 
        marginTop: '20px', 
        padding: '12px 14px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '8px',
        fontSize: '14px',
        color: '#666'
      }}>
        CSV file should match the format of the provided <strong>sample_equipment_data.csv</strong>.
      </div>
    </div>
  );
};

export default UploadForm;
