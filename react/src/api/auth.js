import { instance } from './axios';

export const register = async (username, displayName, password) => {
  const response = await instance.post('/api/auth/register/', {
    username,
    display_name: displayName,
    password
  });
  return response.data;
};

export const login = async (username, password) => {
  const response = await instance.post('/api/auth/login/', {
    username,
    password
  });
  return response.data;
};

export const logout = async (token) => {
  const response = await instance.post('/api/auth/logout/', {}, {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.data;
};

export const getProfile = async (token) => {
  const response = await instance.get('/api/auth/profile/', {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.data;
};

export const updateProfile = async (token, displayName) => {
  const response = await instance.patch('/api/auth/profile/', {
    display_name: displayName
  }, {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.data;
};