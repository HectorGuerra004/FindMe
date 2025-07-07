<script setup>
import { ref } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'
import useAuth from '@/services/auth' // Asegúrate de importar tu hook de autenticación

const sidebarVisible = ref(true)
const isMobile = ref(false)
const { register, error, isLoading } = useAuth()

// Campos del formulario
const nombre = ref('')
const apellido = ref('')
const email = ref('')
const telefono = ref('')
const fechaNacimiento = ref('')
const ubicacion = ref('')
const password = ref('')

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const handleSubmit = async (e) => {
  e.preventDefault()
  const formData = {
    email: email.value,
    password: password.value,
    profile: {
      nombre: nombre.value,
      apellido: apellido.value,
      telefono: telefono.value,
      fecha_nacimiento: fechaNacimiento.value,
      ubicacion: ubicacion.value
    }
  }
  await register(formData)
}
</script>

<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="register-container">
        <h2>Crear cuenta</h2>
        <form @submit="handleSubmit">
          <input v-model="nombre" type="text" placeholder="Nombre" required />
          <input v-model="apellido" type="text" placeholder="Apellido" required />
          <input v-model="email" type="email" placeholder="Correo electrónico" required />
          <input v-model="telefono" type="tel" placeholder="Teléfono" />
          <input v-model="fechaNacimiento" type="date" placeholder="Fecha de nacimiento" />
          <input v-model="ubicacion" type="text" placeholder="Ubicación (País, Estado, Ciudad)" />
          <input v-model="password" type="password" placeholder="Contraseña" required />
          <button type="submit" :disabled="isLoading">Registrarse</button>
        </form>
        <div v-if="error" style="color: red; margin-top: 1rem;">{{ error }}</div>
        <div class="login-link">
          ¿Ya tienes cuenta? <router-link to="/login">Inicia sesión aquí</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: #e1e4e9;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.register-container h2 {
  margin-bottom: 1.5rem;
}

.register-container input {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.register-container button {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
}

.login-link {
  margin-top: 1.5rem;
  font-size: 0.95rem;
}

.login-link a {
  color: #1a1a3c;
  text-decoration: underline;
}
</style>