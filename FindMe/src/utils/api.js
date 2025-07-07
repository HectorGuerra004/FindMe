import axios from 'axios';
const api = axios.create({
  baseURL: "http://192.168.111.79:8000/api/",
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export default api;