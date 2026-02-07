import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { authAPI } from './api';

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(credentials);
      const { token, user } = response.data;
      
      localStorage.setItem('authToken', token);
      localStorage.setItem('user', user);
      
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {/* Animated Background Elements */}
      <div className="bg-animation bg-animation-1"></div>
      <div className="bg-animation bg-animation-2"></div>
      
      {/* Login Card */}
      <div className="login-card">
        <div className="login-header">
          <h2 className="login-title">
            Chemical Equipment Visualizer
          </h2>
          <p className="login-subtitle">
            Please login to access the dashboard
          </p>
        </div>

        {error && (
          <div className="error-message">
            {error}
            <button
              className="error-close"
              onClick={() => setError('')}
            >
              ×
            </button>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <div className="input-wrapper">
              <input
                type="text"
                name="username"
                placeholder="👤 Username"
                value={credentials.username}
                onChange={handleChange}
                required
                disabled={loading}
                className="form-input"
              />
              <div className="input-icon" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? '👁️' : '👁️'}
              </div>
            </div>

            <div className="input-wrapper">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder={showPassword ? "🔑 Password" : "🔒 Password"}
                value={credentials.password}
                onChange={handleChange}
                required
                disabled={loading}
                className="form-input"
              />
              <div className="input-icon" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? '🙈' : '👁️'}
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="login-button"
          >
            {loading ? (
              <span className="button-content">
                <span className="spinner"></span>
                <span>Authenticating...</span>
              </span>
            ) : 'Sign In'}
          </button>
        </form>

        <div className="test-credentials">
          <h4>Test Credentials</h4>
          <div className="credentials-grid">
            <div>
              <strong>Username:</strong>
              <div>admin</div>
            </div>
            <div>
              <strong>Password:</strong>
              <div>admin123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
