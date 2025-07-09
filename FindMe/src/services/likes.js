// src/services/likes.js
import api from '../utils/api'; // Importa tu instancia de Axios ya configurada

// ¡Elimina la importación de getAuthToken!
// import { getAuthToken } => NO NECESARIO

const likesService = {
  async toggleLike(profileId) {
    try {
      // Axios con 'withCredentials: true' se encarga de enviar las cookies.
      const response = await api.post(
        `/likes/toggle/`, // Ruta relativa a tu baseURL de Axios
        { to_profile: profileId }
        // No necesitas headers de Authorization aquí
      );
      return response.data;
    } catch (error) {
      console.error('Error al alternar like:', error.response?.data || error.message);
      throw error;
    }
  },

  async checkIfLiked(profileId) {
    try {
      // Axios con 'withCredentials: true' se encarga de enviar las cookies.
      const response = await api.get(
        `/profiles/${profileId}/is_liked/` // Ruta relativa a tu baseURL de Axios
        // No necesitas headers de Authorization aquí
      );
      return response.data;
    } catch (error) {
      console.error('Error al verificar like:', error.response?.data || error.message);
      // Si la solicitud falla (ej. 401 Unauthorized porque no hay cookie), asumimos que no hay like
      return { is_liked: false }; 
    }
  }
};

export default likesService;