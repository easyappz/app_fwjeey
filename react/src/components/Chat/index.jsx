import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMessages, sendMessage } from '../../api/messages';
import { logout } from '../../api/auth';
import './styles.css';

export const Chat = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  const token = localStorage.getItem('token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    if (!token) {
      navigate('/login');
      return;
    }
    loadMessages();
    const interval = setInterval(loadMessages, 3000);
    return () => clearInterval(interval);
  }, [token, navigate]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadMessages = async () => {
    try {
      setLoading(true);
      const data = await getMessages(token, 50, 0);
      setMessages(data.results.reverse());
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    setSending(true);
    setError('');

    try {
      await sendMessage(token, newMessage);
      setNewMessage('');
      await loadMessages();
    } catch (err) {
      setError(err.response?.data?.error || 'Ошибка отправки сообщения');
    } finally {
      setSending(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout(token);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/login');
    }
  };

  return (
    <div data-easytag="id1-src/components/Chat/index.jsx" className="chat-container">
      <div className="chat-header">
        <div className="chat-title">
          <h1>Групповой чат</h1>
          <span className="user-info">Вы: {user.display_name}</span>
        </div>
        <button onClick={handleLogout} className="logout-button">
          Выйти
        </button>
      </div>
      <div className="messages-container">
        {loading && messages.length === 0 && (
          <div className="loading-message">Загрузка сообщений...</div>
        )}
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.author.id === user.id ? 'own-message' : 'other-message'}`}
          >
            <div className="message-author">{message.author.display_name}</div>
            <div className="message-text">{message.text}</div>
            <div className="message-time">
              {new Date(message.created_at).toLocaleString('ru-RU')}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      {error && <div className="error-banner">{error}</div>}
      <form onSubmit={handleSendMessage} className="message-form">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Введите сообщение..."
          maxLength={2000}
          disabled={sending}
          className="message-input"
        />
        <button type="submit" disabled={sending || !newMessage.trim()} className="send-button">
          {sending ? 'Отправка...' : 'Отправить'}
        </button>
      </form>
    </div>
  );
};