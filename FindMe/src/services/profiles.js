import { ref } from 'vue';
import api from '../utils/api';
import { useRouter } from 'vue-router';

export default function useAuth() {
    const router = useRouter();
    const error = ref('');
    const isLoading = ref(false);
    const user = ref(null); // Asegúrate de tener esta referencia

    // Obtener perfil del usuario autenticado (sesión actual)
    const getProfileData = async () => {
        try {
            const response = await api.get('/complete-profile/');
            console.log('Datos recibidos backend (usuario autenticado):', response.data);
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    // Nueva función: Obtener perfil de un usuario por ID
    const getProfileById = async (userId) => {
        try {
            const response = await api.get(`/public-profiles/${userId}/`);
            console.log(`Datos recibidos backend para usuario ${userId}:`, response.data);
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    return {
        getProfileData,
        getProfileById, // Exportamos la nueva función
        error,
        isLoading,
        user, // Exponer el usuario para que pueda ser utilizado en componentes
    };
}