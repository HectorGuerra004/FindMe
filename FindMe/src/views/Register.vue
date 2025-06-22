
<script setup>
import { ref, computed, onMounted } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'



const sidebarVisible = ref(true)
const isMobile = ref(false)

// Función para actualizar el estado cuando el sidebar emite cambios
const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}


// Datos para las tarjetas
const cards = ref([
  { icon: 'edit_document', title: 'Orden de Produccion', link: '/NewProduction' },
  { icon: 'edit_document', title: 'Orden de Servicio', link: '/NewService'},
  { icon: 'edit_document', title: 'Solicitud de Stock', link: '/NewStock' },
  { icon: 'edit_document', title: 'Formato de memo' },
  { icon: 'edit_document', title: 'Formato de Cotizacion' },
])
</script>

<template>
  <div class="app-container">
    <!-- Contenido principal -->
    <SideBar @state-change="handleSidebarState" />

    <main :class="['main-content', { 'shifted': sidebarVisible && !isMobile }]">
      <!-- Contenedor con borde decorativo -->
      <div class="content-frame">
        <!-- Sección de creación de órdenes -->
        <div class="order-creation-section">
          <h2 class="section-title">Crear Nueva Orden</h2>
          <div class="cards-container">
            <div class="card" v-for="(card, index) in cards" :key="index">
              <div class="card-content">
                <span class="material-icons">{{ card.icon }}</span>
                <div class="card-title">{{ card.title }}</div>
              </div>
              
              <router-link :to="card.link" class="create-order-btn" @click="closeIfMobile">
                <span class="material-icons">add</span> Crear orden
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Espacio para el contenido adicional -->
        <div class="additional-content">
          <router-view />
        </div>
      </div>
      <div class="content-frame">
        <!-- Sección de creación de órdenes -->
        
        <form class="form-search-input" action="">
          <input type="text" placeholder="Buscar..." class="search-input" />
          
        </form>

        <!-- Espacio para el contenido adicional -->
      </div>
      <div class="content-frame">
        <DataTableIndex />
      </div>
    </main>
  </div>
</template>


<style scoped>

</style>