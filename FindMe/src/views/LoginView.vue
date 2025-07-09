<script setup>
import { ref } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'
import useAuth from '@/services/auth' // Asegúrate de importar tu hook de autenticación

const sidebarVisible = ref(true)
const isMobile = ref(false)
const { login, error, isLoading } = useAuth()

const email = ref('')
const password = ref('')

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const handleSubmit = async (e) => {
  e.preventDefault()
  await login(email.value, password.value)
}
</script>

<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="login-container">
        <h2>Iniciar sesión</h2>
        <form @submit="handleSubmit">
          <input v-model="email" type="email" placeholder="Correo electrónico" required />
          <input v-model="password" type="password" placeholder="Contraseña" required />
          <button type="submit" :disabled="isLoading">Entrar</button>
        </form>
        <div v-if="error" style="color: red; margin-top: 1rem;">{{ error }}</div>
        <div class="register-link">
          ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 100px auto;
  padding: 2rem;
  background: #e1e4e9;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.login-container h2 {
  margin-bottom: 1.5rem;
}

.login-container input {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.login-container button {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
}

.register-link {
  margin-top: 1.5rem;
  font-size: 0.95rem;
}

.register-link a {
  color: #1a1a3c;
  text-decoration: underline;
}
</style>
