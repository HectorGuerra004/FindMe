<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="content-frame">
        <h2 class="section-title">Find professionals</h2>
        <div class="search-bar-container">
          <input
            v-model="searchText"
            type="text"
            class="search-bar"
            placeholder="Buscar por nombre, título o ubicación..."
          />
        </div>
        <div v-if="filteredUsers.length === 0" class="no-results-message">
          No se encontraron profesionales que coincidan con tu búsqueda.
        </div>
        <div v-else class="cards-grid">
          <div v-for="user in filteredUsers" :key="user.id" class="card">
            <img :src="user.image" class="card-avatar" :alt="user.name" />
            <div class="card-info">
              <h3>{{ user.name }}</h3>
              <p>{{ user.title }}</p>
              <p class="location">{{ user.location }}</p>
            </div>
            <div class="card-actions">
              <router-link :to="`/profile/${user.id}`" class="connect-button">
                ⌕ Ver
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'
import api from '../utils/api';

const users = ref([])
const searchText = ref('')

const sidebarVisible = ref(true)
const isMobile = ref(false)

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

function normalize(str) {
  return str
    ? str.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu, '')
    : ''
}

const filteredUsers = computed(() => {
  const search = normalize(searchText.value)
  if (!search) return users.value
  return users.value.filter(user => {
    return (
      normalize(user.name).includes(search) ||
      normalize(user.title).includes(search) ||
      normalize(user.location).includes(search)
    )
  })
})

onMounted(async () => {
  try {
    const { data } = await api.get('/profiles/')
    console.log('Perfiles recibidos:', data)
    users.value = data.map(user => ({
      id: user.user_id,
      name: `${user.nombre} ${user.apellido}`,
      title: user.titulo || 'Sin título',
      location: user.ubicacion,
      image: user.img_profile || 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png'
    }))
    if (users.value.length === 0) {
      console.warn('No se encontraron usuarios para mostrar.')
    }
  } catch (error) {
    console.error('Error al obtener perfiles:', error)
  }
})
</script>

<style scoped>
.section-title {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a1a3c;
}
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}
.card {
  background: white;
  padding: 1.5rem;
  border-radius: 24px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.card-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 1rem;
}
.card-info h3 {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}
.card-info p {
  font-size: 0.85rem;
  color: #666;
  margin: 0.25rem 0;
}
.card-actions {
  margin-top: 1.5rem;
  width: 100%;
  display: flex;
  justify-content: center;
}
.connect-button {
  background: #c246a1;
  color: white;
  border: none;
  border-radius: 16px;
  padding: 0.6rem 1.5rem;
  margin-top: 0;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(194, 70, 161, 0.08);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s, transform 0.2s;
  text-decoration: none;
}
.connect-button:hover {
  background: #b04cc8;
  transform: translateY(-2px) scale(1.04);
}
.search-bar-container {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}
.search-bar {
  width: 100%;
  max-width: 400px;
  padding: 0.7rem 1.2rem;
  border: 1px solid #e0e0e0;
  border-radius: 16px;
  font-size: 1rem;
  outline: none;
  box-shadow: 0 2px 8px rgba(194, 70, 161, 0.04);
  transition: border 0.2s;
}
.search-bar:focus {
  border-color: #c246a1;
}
.no-results-message {
  text-align: center;
  color: #b04cc8;
  font-size: 1.1rem;
  margin: 2rem 0 2.5rem 0;
  font-weight: 500;
}
</style>
