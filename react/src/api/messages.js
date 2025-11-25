import { instance } from './axios';

export const getMessages = async (token, limit = 50, offset = 0) => {
  const response = await instance.get('/api/messages/', {
    params: { limit, offset },
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.data;
};

export const sendMessage = async (token, text) => {
  const response = await instance.post('/api/messages/', {
    text
  }, {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  return response.data;
};