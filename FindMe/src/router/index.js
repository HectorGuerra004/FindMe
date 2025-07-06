import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import LandingPage from '../views/LandingPage.vue';
import ConfigurationView from '../views/ConfigurationView.vue';
import UserProfile from '../views/UserProfile.vue';
import CompleteProfile from '@/views/completeProfile.vue';


const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/', name: 'Landing', component: LandingPage },
  { path: '/configuration', name: 'Configuration', component: ConfigurationView },
  { path: '/profile', name: 'UserProfile', component: UserProfile },
  { path: '/completeProfile', name: 'CompleteProfile', component: CompleteProfile },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
