import React, { useState, useEffect } from 'react';
import TransactionList from '../components/TransactionList';
import { authService } from '../services/api';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        setLoading(true);
        const response = await authService.getCurrentUser();
        setUser(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to load user data. Please login again.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome, {user?.first_name || 'User'}</h1>
        <p>Manage your finances with ease</p>
      </div>
      
      <div className="dashboard-summary">
        <div className="summary-card">
          <h3>Total Income</h3>
          <p className="amount income">$0.00</p>
        </div>
        <div className="summary-card">
          <h3>Total Expenses</h3>
          <p className="amount expense">$0.00</p>
        </div>
        <div className="summary-card">
          <h3>Balance</h3>
          <p className="amount balance">$0.00</p>
        </div>
      </div>
      
      <div className="dashboard-content">
        <TransactionList />
      </div>
    </div>
  );
};

export default Dashboard;
