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
      localStorage.setItem('user', JSON.stringify(response.data.user));
      router.push({ name: 'Landing' });
    } else {
      throw new Error('Información de usuario no recibida');
    }
  } catch (err) {
    console.error('Error al iniciar sesión:', err.response ? err.response.data : err.message);

    // --- ¡AQUÍ ESTÁ EL CAMBIO CLAVE! ---
    if (err.response && err.response.data) {
      // Priorizar 'non_field_errors' para errores de credenciales inválidas
      if (err.response.data.non_field_errors && err.response.data.non_field_errors.length > 0) {
        error.value = err.response.data.non_field_errors[0];
      }
      // Si hubiera errores específicos de campo (ej: 'email' o 'password')
      else if (err.response.data.email && err.response.data.email.length > 0) {
        error.value = err.response.data.email[0];
      } else if (err.response.data.password && err.response.data.password.length > 0) {
        error.value = err.response.data.password[0];
      }
      // Mensaje genérico si no se encuentra un error específico en la respuesta
      else {
        error.value = 'Error desconocido al iniciar sesión. Por favor, intenta de nuevo.';
      }
    } else {
      // Manejar errores de red o cualquier otro error sin respuesta del servidor
      error.value = 'No se pudo conectar al servidor. Verifica tu conexión a internet.';
    }
    // --- FIN DEL CAMBIO CLAVE ---

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