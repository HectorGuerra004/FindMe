import { ref } from 'vue';
import api from '../utils/api';
import { useRouter } from 'vue-router';

export default function useAuth() {
    const router = useRouter();
    const error = ref('');
    const isLoading = ref(false);
    const user = ref(null); // Para almacenar la información del usuario si el backend la devuelve

    const login = async (email, password) => {
        if (!email || !password) {
            error.value = 'Todos los campos son obligatorios';
            return;
        }
        try {
            isLoading.value = true;
            const response = await api.post('/login/', { email, password });

            if (response.data.user) {
                user.value = response.data.user;
                router.push({ name: 'Landing' }); // Asegúrate que el nombre de tu ruta coincida
            } else {
                throw new Error('Información de usuario no recibida');
            }
        } catch (err) {
            console.error('Error al iniciar sesión:', err.response ? err.response.data : err.message);
            error.value = err.response?.data?.errors?.[0] || 'Error desconocido al iniciar sesión.';
        } finally {
            isLoading.value = false;
        }
    };

    const register = async (formData) => {
        try {
            isLoading.value = true;
            error.value = '';

            const response = await api.post('/register/', formData);

            if (response.data.email) {
                user.value = response.data;
                router.push({ name: 'Landing' });
            } else {
                throw new Error('Información de usuario no recibida');
            }
        } catch (err) {
            // Mostrar todos los errores del backend (pueden venir como objeto)
            if (err.response && err.response.data) {
                // Si es un objeto de errores, conviértelo a string legible
                if (typeof err.response.data === 'object') {
                    error.value = Object.values(err.response.data).flat().join(' ');
                } else {
                    error.value = err.response.data;
                }
            } else {
                error.value = 'Error desconocido al registrarse.';
            }
            console.error('Error al registrarse:', err.response ? err.response.data : err.message);
        } finally {
            isLoading.value = false;
        }
    };

    const logout = async () => {
        await api.post('/auth/logout');
        localStorage.removeItem('user');
        router.push({ name: 'Login' });
    };

    return {
        login,
        register,
        logout,
        error,
        isLoading,
        user, // Exponer el usuario para que pueda ser utilizado en componentes
    };
}