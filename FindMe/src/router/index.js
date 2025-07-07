import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import LandingPage from '../views/LandingPage.vue';
import ConfigurationView from '../views/ConfigurationView.vue';
import UserProfile from '../views/UserProfile.vue';
import CompleteProfile from '@/views/completeProfile.vue';
import { user } from '@/stores/user.js'; // Ajusta la ruta según tu estructura


const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/', name: 'Landing', component: LandingPage },
  { path: '/configuration', name: 'Configuration', component: ConfigurationView },
  
  // Perfil dinámico con parámetro ID
  { 
    path: '/profile/:id', 
    name: 'UserProfile', 
    component: UserProfile,
    props: true // Permite pasar el parámetro como prop
  },
  
  // Mantenemos la ruta sin parámetro para redirección
  {
  path: '/profile',
  redirect: () => {
    if (user.value && user.value.id) {
      return { name: 'UserProfile', params: { id: user.value.id } };
    } else {
      // Si no está logueado, por ejemplo, redirige al login
      return { name: 'Login' };
    }
  }
},

  { path: '/completeProfile', name: 'CompleteProfile', component: CompleteProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;