import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';

const LoginPage = () => {
  const [loginSuccess, setLoginSuccess] = useState(false);

  const handleLoginSuccess = (data) => {
    setLoginSuccess(true);
    // In a real app, you would redirect to the dashboard here
    // or use React Router to navigate
    window.location.href = '/dashboard';
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>Finance Tracker</h1>
        <p>Manage your personal finances with ease</p>
        
        {loginSuccess ? (
          <div className="success-message">
            Login successful! Redirecting...
          </div>
        ) : (
          <LoginForm onLoginSuccess={handleLoginSuccess} />
        )}
        
        <div className="login-footer">
          <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
