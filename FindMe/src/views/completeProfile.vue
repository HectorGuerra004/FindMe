<script setup>
import { ref } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'
import useAuth from '@/services/auth'
import { user } from '@/stores/user'

const sidebarVisible = ref(true)
const isMobile = ref(false)
const { completarPerfil, error, isLoading } = useAuth()


const sobreMi = ref('')

// Campos dinámicos
const educacion = ref([''])
const habilidades = ref([''])
const experiencia = ref([''])

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const addEducacion = () => educacion.value.push('')
const removeEducacion = (idx) => educacion.value.splice(idx, 1)

const addHabilidad = () => habilidades.value.push('')
const removeHabilidad = (idx) => habilidades.value.splice(idx, 1)

const addExperiencia = () => experiencia.value.push('')
const removeExperiencia = (idx) => experiencia.value.splice(idx, 1)
console.log(user.value.id)

const handleSubmit = async (e) => {
  e.preventDefault()
  const formData = {
    user: user.value.id, // <-- Aquí agregas el ID del usuario
    
    sobre_mi: sobreMi.value,
    educacion: educacion.value.filter(e => e.trim() !== ''),
    habilidades: habilidades.value.filter(h => h.trim() !== ''),
    experiencia: experiencia.value.filter(ex => ex.trim() !== '')
  }
  await completarPerfil(formData)
}
</script>

<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="register-container">
        <h2>Completa tu perfil</h2>
        <form @submit="handleSubmit">
          <textarea v-model="sobreMi" placeholder="Describe un poco tu perfil" required></textarea>

          <label>Educación</label>
          <div v-for="(edu, idx) in educacion" :key="'edu-' + idx" class="input-group">
            <input v-model="educacion[idx]" type="text" placeholder="Ej: Universidad, carrera, año..." required />
            <button type="button" class="btn-eliminar" @click="removeEducacion(idx)" v-if="educacion.length > 1">Eliminar</button>
          </div>
          <button type="button" class="btn-agregar" @click="addEducacion">Agregar otra educación</button>

          <label>Habilidades</label>
          <div v-for="(hab, idx) in habilidades" :key="'hab-' + idx" class="input-group">
            <input v-model="habilidades[idx]" type="text" placeholder="Ej: Python, Trabajo en equipo..." required />
            <button type="button" class="btn-eliminar" @click="removeHabilidad(idx)" v-if="habilidades.length > 1">Eliminar</button>
          </div>
          <button type="button" class="btn-agregar" @click="addHabilidad">Agregar otra habilidad</button>

          <label>Experiencia laboral</label>
          <div v-for="(exp, idx) in experiencia" :key="'exp-' + idx" class="input-group">
            <input v-model="experiencia[idx]" type="text" placeholder="Ej: Empresa, puesto, años..." required />
            <button type="button" class="btn-eliminar" @click="removeExperiencia(idx)" v-if="experiencia.length > 1">Eliminar</button>
          </div>
          <button type="button" class="btn-agregar" @click="addExperiencia">Agregar otra experiencia</button>

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
  max-width: 800px;
  margin: 100px auto;
  padding: 2rem;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}
.register-container h2 {
  margin-bottom: 1.5rem;
}
.register-container input,
.register-container textarea {
  display: block;
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}
.register-container label {
  font-weight: bold;
  margin-top: 1rem;
  display: block;
}
.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}
.input-group input {
  flex: 1;
}
.input-group button {
  margin-left: 0.5rem;
}

.register-container button[type="submit"] {
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

.btn-agregar {
  background: #27ae60;
  color: #fff;
  border: none;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  margin-top: 0.2rem;
  margin-left: 0;
  text-align: left;
  display: block;
  font-weight: bold;
  cursor: pointer;
}
.btn-agregar:hover {
  background: #219150;
}
.btn-eliminar {
  background: #e74c3c;
  color: #fff;
  border: none;
  padding: 0.3rem 0.8rem;
  border-radius: 6px;
  margin-left: 0.5rem;
  font-weight: bold;
  cursor: pointer;
}
.btn-eliminar:hover {
  background: #c0392b;
}
.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}
.input-group input {
  flex: 1;
}
.register-container button[type="submit"] {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
}
</style>