import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';

export const Home = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/chat');
    }
  }, [navigate]);

  return (
    <div data-easytag="id1-src/components/Home/index.jsx" className="home-container">
      <div className="home-content">
        <h1>Добро пожаловать в групповой чат</h1>
        <p>Общайтесь с другими пользователями в реальном времени</p>
        <div className="home-buttons">
          <button onClick={() => navigate('/login')} className="home-button primary">
            Войти
          </button>
          <button onClick={() => navigate('/register')} className="home-button secondary">
            Зарегистрироваться
          </button>
        </div>
      </div>
    </div>
  );
};