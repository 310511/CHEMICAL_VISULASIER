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
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Animated Background Elements */}
      <div style={{
        position: 'absolute',
        top: '-50%',
        left: '-50%',
        width: '200%',
        height: '200%',
        background: 'radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%)',
        animation: 'float 6s ease-in-out infinite'
      }} />
      <div style={{
        position: 'absolute',
        top: '-50%',
        left: '-50%',
        width: '200%',
        height: '200%',
        background: 'radial-gradient(circle, rgba(118, 75, 162, 0.1) 0%, transparent 70%)',
        animation: 'float 8s ease-in-out infinite reverse'
      }} />
      
      {/* Login Card */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '40px',
        boxShadow: '0 25px 50px rgba(0, 0, 0, 0.3)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        zIndex: 10,
        maxWidth: '400px',
        width: '100%',
        position: 'relative',
        animation: 'slideIn 0.5s ease-out'
      }}>
        <div style={{
          textAlign: 'center',
          marginBottom: '30px'
        }}>
          <h2 style={{
            fontSize: '2rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, #667eea, #764ba2)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            color: 'transparent',
            textShadow: '2px 2px 4px rgba(0, 0, 0, 0.1)',
            marginBottom: '10px'
          }}>
            Chemical Equipment Visualizer
          </h2>
          <p style={{
            color: '#6c757d',
            fontSize: '1rem',
            marginBottom: '30px'
          }}>
            Please login to access the dashboard
          </p>
        </div>

        {error && (
          <div style={{
            background: 'linear-gradient(135deg, #f8d7da, #f5c6cb)',
            color: '#721c24',
            padding: '12px 16px',
            borderRadius: '8px',
            marginBottom: '20px',
            fontSize: '14px',
            border: '1px solid #f5c6cb',
            animation: 'shake 0.5s ease-in-out'
          }}>
            {error}
            <button
              onClick={() => setError('')}
              style={{
                background: 'none',
                border: 'none',
                color: '#721c24',
                float: 'right',
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

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '20px' }}>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                name="username"
                placeholder="👤 Username"
                value={credentials.username}
                onChange={handleChange}
                required
                disabled={loading}
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #dee2e6',
                  borderRadius: '12px',
                  fontSize: '16px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => e.target.style.borderColor = '#667eea'}
              />
              <div style={{
                position: 'absolute',
                right: '20px',
                top: '50%',
                transform: 'translateY(-50%)',
                cursor: 'pointer',
                color: '#6c757d',
                fontSize: '14px',
                userSelect: 'none'
              }}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '👁️' : '👁️'}
              </div>
            </div>

            <div style={{ position: 'relative', marginBottom: '20px' }}>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder={showPassword ? "🔑 Password" : "🔒 Password"}
                value={credentials.password}
                onChange={handleChange}
                required
                disabled={loading}
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #dee2e6',
                  borderRadius: '12px',
                  fontSize: '16px',
                  background: 'rgba(255, 255, 255, 0.1)',
                  transition: 'all 0.3s ease',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
                onFocus={(e) => e.target.style.borderColor = '#667eea'}
              />
              <div style={{
                position: 'absolute',
                right: '20px',
                top: '50%',
                transform: 'translateY(-50%)',
                cursor: 'pointer',
                color: '#6c757d',
                fontSize: '14px',
                userSelect: 'none'
              }}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? '🙈' : '👁️'}
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '16px 24px',
              border: 'none',
              borderRadius: '12px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
              background: loading 
                ? 'linear-gradient(135deg, #6c757d, #495057)' 
                : 'linear-gradient(135deg, #667eea, #764ba2)',
              color: 'white',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
              position: 'relative',
              overflow: 'hidden'
            }}
          >
            {loading ? (
              <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px'
              }}>
                <span style={{
                  width: '20px',
                  height: '20px',
                  border: '3px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '50%',
                  borderTop: '3px solid transparent',
                  animation: 'spin 1s linear infinite'
                }}></span>
                <span>Authenticating...</span>
              </span>
            ) : 'Sign In'}
          </button>
        </form>

        <div style={{
          textAlign: 'center',
          marginTop: '30px',
          padding: '20px',
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <h4 style={{
            margin: '0 0 10px 0',
            color: '#6c757d',
            fontSize: '14px',
            fontWeight: '600'
          }}>
            Test Credentials
          </h4>
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '10px',
            fontSize: '13px'
          }}>
            <div>
              <strong>Username:</strong>
              <div style={{ color: '#495057' }}>admin</div>
            </div>
            <div>
              <strong>Password:</strong>
              <div style={{ color: '#495057' }}>admin123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
