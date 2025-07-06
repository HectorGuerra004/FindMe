import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import LandingPage from '../views/LandingPage.vue';
import ConfigurationView from '../views/ConfigurationView.vue';
import UserProfile from '../views/UserProfile.vue';

const routes = [
  { path: '/', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/landing', name: 'Landing', component: LandingPage },
  { path: '/configuration', name: 'Configuration', component: ConfigurationView },
  { path: '/profile', name: 'UserProfile', component: UserProfile },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
