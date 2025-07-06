<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <div class="content-frame">
        <h2 class="section-title">Configuración</h2>
        <div class="config-content">
          <p>Aquí puedes agregar la configuración de tu usuario, preferencias, etc.</p>
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
</script>

<style scoped>
.section-title {
  margin-bottom: 2rem;
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a1a3c;
}
.config-content {
  font-size: 1rem;
  color: #333;
}
.app-container {
  display: flex;
  font-family: 'Inter', sans-serif;
  background: #f1f3fc;
  height: 100vh;
}

.sidebar {
  width: 220px;
  background: #ffffff;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: 1px solid #dcdcdc;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1a1a3c;
}

.logo span {
  color: #b04cc8;
}

nav ul {
  list-style: none;
  padding: 0;
}

nav ul li {
  margin: 1rem 0;
}

nav button {
  width: 100%;
  background: none;
  border: none;
  font-size: 1rem;
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  transition: background 0.3s;
}

nav button.active,
nav button:hover {
  background: #1a1a3c;
  color: white;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.main-content {
  flex: 1;
  padding: 6rem;
}

.main-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.search-bar input {
  flex: 1;
  padding: 0.5rem;
  border-radius: 12px;
  border: 1px solid #ccc;
}

.icon-button {
  background: #1a1a3c;
  color: white;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
}

.filter-bar,
.user-menu {
  display: flex;
  gap: 1rem;
}

.filter-button,
.location-button {
  background: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  border: 1px solid #ccc;
}

.outgoing-button {
  background: #1a1a3c;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  border: none;
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

.card-info h3 {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.card-info p {
  font-size: 0.85rem;
  color: #666;
  margin: 0.25rem 0;
}
</style>
