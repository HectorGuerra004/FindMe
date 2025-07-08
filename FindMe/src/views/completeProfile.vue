<script setup>
import { ref, onMounted } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'
import useAuth from '@/services/auth'

const sidebarVisible = ref(true)
const isMobile = ref(false)
const { completarPerfil, error, isLoading, getProfileData } = useAuth()

const sobreMi = ref('')

// Campos dinámicos con estructura de objetos
const educacion = ref([{ titulo: '', institucion: '', campo_estudio: '' }])
const habilidades = ref([{ nombre_skill: '', nivel: '' }])
const experiencia = ref([{ empresa: '', puesto: '', ubicacion_exp: '', inicio_exp: '', fin_exp: '' }])

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const addEducacion = () => educacion.value.push({ titulo: '', institucion: '', campo_estudio: '' })
const removeEducacion = (idx) => { if (educacion.value.length > 1) educacion.value.splice(idx, 1) }

const addHabilidad = () => habilidades.value.push({ nombre_skill: '', nivel: '' })
const removeHabilidad = (idx) => { if (habilidades.value.length > 1) habilidades.value.splice(idx, 1) }

const addExperiencia = () => experiencia.value.push({ empresa: '', puesto: '', ubicacion_exp: '', inicio_exp: '', fin_exp: '' })
const removeExperiencia = (idx) => { if (experiencia.value.length > 1) experiencia.value.splice(idx, 1) }

// Carga datos del backend y setea los refs
const cargarDatosPerfil = async () => {
  try {
    const data = await getProfileData()
    if (data) {
      sobreMi.value = data.sobre_mi || ''
      educacion.value = (data.educacion && data.educacion.length > 0)
        ? data.educacion.map(item => ({
          titulo: item.titulo || '',
          institucion: item.institucion || '',
          campo_estudio: item.campo_estudio || ''
        }))
        : [{ titulo: '', institucion: '', campo_estudio: '' }]

      habilidades.value = (data.habilidades && data.habilidades.length > 0)
        ? data.habilidades.map(item => ({
          nombre_skill: item.nombre_skill || '',
          nivel: item.nivel || ''
        }))
        : [{ nombre_skill: '', nivel: '' }]

      experiencia.value = (data.experiencia && data.experiencia.length > 0)
        ? data.experiencia.map(item => ({
          empresa: item.empresa || '',
          puesto: item.puesto || '',
          ubicacion_exp: item.ubicacion_exp || '',
          inicio_exp: item.inicio_exp || '',
          fin_exp: item.fin_exp || ''
        }))
        : [{ empresa: '', puesto: '', ubicacion_exp: '', inicio_exp: '', fin_exp: '' }]
    }
  } catch (err) {
    console.error('Error al cargar perfil:', err)
  }
}

onMounted(() => {
  cargarDatosPerfil()
})

const handleSubmit = async (e) => {
  e.preventDefault()

  const filteredEducacion = educacion.value.filter(e =>
    e.titulo.trim() !== '' || e.institucion.trim() !== '' || e.campo_estudio.trim() !== ''
  )

  const filteredHabilidades = habilidades.value.filter(h =>
    h.nombre_skill.trim() !== '' || h.nivel !== ''
  )

  const filteredExperiencia = experiencia.value
    .filter(ex => ex.empresa.trim() !== '' || ex.puesto.trim() !== '')
    .map(ex => ({
      ...ex,
      inicio_exp: ex.inicio_exp === '' ? null : ex.inicio_exp,
      fin_exp: ex.fin_exp === '' ? null : ex.fin_exp,
      ubicacion_exp: ex.ubicacion_exp || '',
    }))

  const formData = {
    sobre_mi: sobreMi.value,
    educacion: filteredEducacion,
    experiencia: filteredExperiencia,
    habilidades: filteredHabilidades
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
          <label>Acerca de ti</label>
          <textarea v-model="sobreMi" placeholder="Describe un poco tu perfil profesional" required></textarea>

          <label>Educación</label>
          <div v-for="(edu, idx) in educacion" :key="'edu-' + idx" class="education-group">
            <div class="input-row">
              <div class="input-column">
                <label>Título</label>
                <input v-model="edu.titulo" type="text" placeholder="Ej: Licenciatura en Informática" required />
              </div>
              <div class="input-column">
                <label>Institución</label>
                <input v-model="edu.institucion" type="text" placeholder="Ej: Universidad Nacional" required />
              </div>
            </div>
            <div class="input-column">
              <label>Campo de estudio</label>
              <input v-model="edu.campo_estudio" type="text" placeholder="Ej: Ciencias de la Computación" />
            </div>
            <button type="button" class="btn-eliminar" @click="removeEducacion(idx)"
              v-if="educacion.length > 1">Eliminar</button>
          </div>
          <button type="button" class="btn-agregar" @click="addEducacion">Agregar otra educación</button>
          <!-- HABILIDADES -->
          <label>Habilidades</label>

          <div v-for="(hab, idx) in habilidades" :key="'hab-' + idx" class="skill-group">
            <div class="input-row">
              <div class="input-column">
                <label>Nombre</label>
                <input v-model="hab.nombre_skill" type="text" placeholder="Ej: Python, React" required />
              </div>
              <div class="input-column">
                <label>Nivel</label>
                <select v-model="hab.nivel" required>
                  <option value="" disabled>Seleccionar nivel</option>
                  <option value="Básico">Básico</option>
                  <option value="Intermedio">Intermedio</option>
                  <option value="Avanzado">Avanzado</option>
                </select>
              </div>
            </div>
            <button type="button" class="btn-eliminar" @click="removeHabilidad(idx)"
              v-if="habilidades.length > 1">Eliminar</button>
          </div>
          <button type="button" class="btn-agregar" @click="addHabilidad">Agregar otra habilidad</button>

          <!-- EXPERIENCIA -->
          <label>Experiencia</label>

          <div v-for="(exp, idx) in experiencia" :key="'exp-' + idx" class="experience-group">
            <div class="input-row">
              <div class="input-column">
                <label>Empresa</label>
                <input v-model="exp.empresa" type="text" placeholder="Ej: Google, Microsoft" required />
              </div>
              <div class="input-column">
                <label>Puesto</label>
                <input v-model="exp.puesto" type="text" placeholder="Ej: Desarrollador Frontend" required />
              </div>
              <div class="input-column">
                <label>Ubicación</label>
                <input v-model="exp.ubicacion_exp" type="text" placeholder="Ej: Ciudad, País" />
              </div>

            </div>
            <div class="input-row-experience">
              <div class="input-column">
                <label>Fecha de inicio</label>
                <input v-model="exp.inicio_exp" type="date" required />
              </div>
              <div class="input-column">
                <label>Fecha de fin</label>
                <input v-model="exp.fin_exp" type="date" />
                <small>(Dejar vacío si es actual)</small>
              </div>
            </div>
            <button type="button" class="btn-eliminar" @click="removeExperiencia(idx)"
              v-if="experiencia.length > 1">Eliminar</button>
          </div>

          <button type="button" class="btn-agregar" @click="addExperiencia">Agregar otra experiencia</button>

          <button type="submit" :disabled="isLoading" class="submit-btn">
            {{ isLoading ? 'Guardando...' : 'Guardar perfil' }}
          </button>
        </form>
        <div v-if="error" class="error-message">{{ error }}</div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 800px;
  margin: 10px auto;
  padding: 2rem;
  background: #e1e4e9;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: left;
}

.register-container h2 {
  margin-bottom: 1.5rem;
  text-align: center;
}

label {
  display: block;
  font-weight: bold;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.input-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.input-row-experience {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.input-column {
  flex: 1;
}

.education-group,
.skill-group,
.experience-group {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  position: relative;
}

.btn-agregar {
  background: #27ae60;
  color: #fff;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  margin-top: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  display: block;
  width: auto;
}

.btn-agregar:hover {
  background: #219150;
}

.btn-eliminar {
  background: #e74c3c;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.btn-eliminar:hover {
  background: #c0392b;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 1.5rem;
}

.submit-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-top: 1.5rem;
  padding: 1rem;
  background: #ffeeee;
  border-radius: 8px;
  text-align: center;
}

small {
  display: block;
  color: #666;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

@media (max-width: 590px) {

  .btn-eliminar {
    padding: 0.2rem 0.5rem;
  }

  .input-row-experience {
    display: block;
  }

}
</style>