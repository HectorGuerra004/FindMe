import { ref } from 'vue';
import api from '../utils/api';
import { user } from '../stores/user.js'

import { useRouter } from 'vue-router';

export default function useAuth() {
  const router = useRouter();
  const error = ref('');
  const isLoading = ref(false);

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

        // Guardar usuario en localStorage para persistencia
        localStorage.setItem('user', JSON.stringify(response.data.user));

        router.push({ name: 'Landing' }); // Ajusta el nombre de la ruta según corresponda
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

  const completarPerfil = async (formData) => {
    try {
      isLoading.value = true;
      error.value = '';
      console.log('Datos del formulario:', formData);

      const response = await api.patch('/complete-profile/', formData);

      if (response.status === 200 || response.status === 204) {
        router.push({ name: 'Landing' });
      } else {
        throw new Error('No se recibieron datos del servidor');
      }

    } catch (err) {
      if (err.response) {
        console.error('Error del backend:', err.response.data);

        if (err.response.status === 400) {
          const errors = [];

          for (const key in err.response.data) {
            if (Array.isArray(err.response.data[key])) {
              errors.push(...err.response.data[key]);
            } else {
              errors.push(err.response.data[key]);
            }
          }

          error.value = errors.join('. ');
        } else {
          error.value = `Error del servidor: ${err.response.status}`;
        }
      } else if (err.request) {
        error.value = 'No se recibió respuesta del servidor';
      } else {
        error.value = err.message || 'Error desconocido al completar el perfil';
      }
    } finally {
      isLoading.value = false;
    }
  };


  const getProfileData = async () => {
    try {
      const response = await api.get('/complete-profile/')
      console.log('Datos recibidos backend:', response.data)

      return response.data
    } catch (error) {
      throw error
    }
  }


  const logout = async () => {
    await api.post('/auth/logout');
    user.value = null

    localStorage.removeItem('user');
    router.push({ name: 'Login' });
  };

  return {
    login,
    register,
    completarPerfil,
    logout,
    getProfileData,
    error,
    isLoading,
    user, // Exponer el usuario para que pueda ser utilizado en componentes
  };
}