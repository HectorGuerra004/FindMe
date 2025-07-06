import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:8000/api/", // Usa variables de entorno
  withCredentials: true, // ¡IMPORTANTE! Permite el envío de cookies de origen cruzado

  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

export default api;