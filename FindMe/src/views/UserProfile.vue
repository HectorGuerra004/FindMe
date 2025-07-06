<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="content-frame">
        <h2 class="section-title">Perfil de usuario</h2>
        <div class="cards-grid">
          <div v-for="user in users" :key="user.id" class="card">
            <img :src="user.image" class="card-avatar" :alt="user.name" />
            <div class="card-info">
              <h3>{{ user.name }}</h3>
              <p>{{ user.title }}</p>
              <p class="location">{{ user.location }}</p>
            </div>
            <div class="card-actions">
              <button class="connect-button">Connect</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'

const sidebarVisible = ref(true)
const isMobile = ref(false)

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const users = ref([
  {
    id: 1,
    name: 'Nedy 70D8&',
    title: 'Networking, Wide VNet Cotingoh',
    location: '32.10.00k',
    image: 'https://via.placeholder.com/80'
  },
  {
    id: 2,
    name: 'Ned 765086',
    title: 'Networking, Wide VNet Polingri',
    location: '9.84.00ck',
    image: 'https://via.placeholder.com/80'
  },
  {
    id: 3,
    name: 'Nel eading 6',
    title: 'VNet Planner, Wide VNet Polingri',
    location: '52.02.01rk',
    image: 'https://via.placeholder.com/80'
  },
  {
    id: 4,
    name: 'Nanlec B16a',
    title: 'VNet Admin, Wide VNet Polingri',
    location: '50.01.5trk',
    image: 'https://via.placeholder.com/80'
  },
])
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
.connect-button {
  background: #c246a1;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 0.5rem 1rem;
  margin-top: 0.5rem;
}
</style>
