<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { shifted: sidebarVisible && !isMobile }]">
      <div class="profile-page">
        <!-- Header: Avatar, Details, Like Buttons -->
        <section class="profile-header">
          <div class="user-info">
            <div class="avatar-wrapper" style="position: relative; display: inline-block;">
              <img
                class="avatar"
                :src="userAvatar || 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png'"
                alt="User Avatar"
              />
              <div class="avatar-overlay" @click="onEditAvatar">
                <span class="avatar-pencil">✎</span>
              </div>
            </div>
            <div class="details details-row">
              <h2>Jane Doe</h2>
              <p class="location">San Francisco, CA</p>
              <div class="bio-like-row">
                <p class="bio">Experienced software engineer passionate about building innovative solutions.</p>
                <div class="action-buttons action-buttons-right">
                  <button class="btn-like" @click="onLikeProfile">
                    👍 Like
                  </button>
                </div>
              </div>
            </div>
          </div>
          <button class="edit-profile-btn" title="Editar perfil" @click="onEditProfile">
            ✎ Editar perfil
          </button>
        </section>

        <!-- Main Content -->
        <section class="profile-main">
          <div class="left-column">
            <!-- Portfolio Card -->
            <div class="card">
              <h3>Portfolio</h3>
              <div class="portfolio-item">
                <span class="icon">🎬</span>
                <div>
                  <p>Project Demo</p>
                  <p class="item-subtitle">Short description or link</p>
                </div>
              </div>
            </div>

            <!-- Education Card -->
            <div class="card">
              <h3>Education</h3>
              <ul class="edu-list">
                <li><span class="dot purple"></span> Python - advanced</li>
                <li><span class="dot red"></span> Javascript - intermediate</li>
                <li><span class="dot gray"></span> Matlab - inato</li>
                <li><span class="dot blue"></span> Android - basic</li>
                <li><span class="dot pink"></span> UX Design - basic</li>
                <li><span class="dot green"></span> ML Design - basic</li>
              </ul>
            </div>
          </div>

          <div class="right-column">
            <!-- Skills Card -->
            <div class="card">
              <h3>Skills</h3>
              <p>Preolicy Danaile</p>
            </div>

            <!-- Expanded Work Experience Card -->
            <div class="card work-experience">
              <h3>Work Experience</h3>
              <ul class="work-list lined">
                <li>
                  <div class="job-entry">
                    <strong>Acme Corp</strong> — Senior Developer<br />
                    New York, NY<br />
                    Jan 2020 — Present
                  </div>
                </li>
                <li>
                  <div class="job-entry">
                    <strong>BetaTech</strong> — Software Engineer<br />
                    San Francisco, CA<br />
                    Jun 2017 — Dec 2019
                  </div>
                </li>
                <li>
                  <div class="job-entry">
                    <strong>Gamma LLC</strong> — Junior Developer<br />
                    Remote<br />
                    Aug 2015 — May 2017
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SideBar from '@/components/sideBar/SideBar.vue'

const sidebarVisible = ref(true)
const isMobile = ref(false)
const userAvatar = ref('')

// Maneja el estado del sidebar
const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

// --- FUNCIONALIDAD DE BOTONES ---
// Aquí puedes implementar la lógica real de cada acción

// 1. Editar foto de perfil
// Llama a un modal, input file o navega a una vista de edición de avatar
function onEditAvatar() {
  // TODO: Abrir modal/input para subir nueva foto de perfil
  // Ejemplo: mostrar un input file y actualizar userAvatar
  alert('Funcionalidad para editar la foto de perfil (por implementar)')
}

// 2. Editar perfil completo
// Puede abrir un modal, navegar a otra ruta o mostrar un formulario editable
function onEditProfile() {
  // TODO: Navegar a /profile/edit o abrir modal de edición
  alert('Funcionalidad para editar el perfil completo (por implementar)')
}

// 3. Like al perfil
// Puede hacer una petición a la API para dar like y actualizar el estado
function onLikeProfile() {
  // TODO: Llamar a la API para dar like y mostrar feedback
  alert('Funcionalidad de Like (por implementar)')
}
</script>

<style scoped>
.profile-page {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: #f4f6f9;
  min-height: 100vh;
}
.profile-header {
  position: relative;
}
.profile-header .user-info {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
  position: relative;
}
.edit-profile-btn {
  position: absolute;
  top: 1.5rem;
  right: 2rem;
  z-index: 2;
  background: linear-gradient(90deg, #3c1650 0%, #901d6a 100%);
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 0.5rem 1.2rem 0.5rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 8px rgba(60, 22, 80, 0.10);
  cursor: pointer;
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
}
.edit-profile-btn:hover {
  filter: brightness(1.08);
  transform: scale(1.07);
  box-shadow: 0 6px 18px 0 rgba(60, 22, 80, 0.18);
}
@media (max-width: 700px) {
  .edit-profile-btn {
    position: static;
    margin-bottom: 1rem;
    width: 100%;
    justify-content: center;
  }
}
.avatar-wrapper {
  position: relative;
  display: inline-block;
  background: linear-gradient(135deg, #3c1650 0%, #901d6a 100%);
  padding: 6px;
  border-radius: 50%;
  box-shadow: 0 6px 24px 0 rgba(139, 96, 211, 0.18), 0 1.5px 6px 0 rgba(90, 174, 240, 0.10);
  transition: box-shadow 0.3s, background 0.3s, transform 0.3s;
}
.avatar-wrapper:hover {
  box-shadow: 0 12px 40px 0 rgba(60, 22, 80, 0.45), 0 4px 16px 0 rgba(144, 29, 106, 0.25);
  background: linear-gradient(135deg, #901d6a 0%, #3c1650 100%);
  transform: scale(1.07) rotate(-2deg);
}
.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(30, 30, 30, 0.55);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}
.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
  pointer-events: auto;
}
.avatar-pencil {
  color: #fff;
  font-size: 2.2rem;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.3s, transform 0.3s;
}
.avatar-wrapper:hover .avatar-pencil {
  opacity: 1;
  transform: translateY(0);
}
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(139, 96, 211, 0.10);
  background: #fff;
  object-fit: cover;
}
.details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.details-row {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}
.bio-like-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}
.bio-like-row .bio {
  margin: 0.5rem 0;
  font-size: 0.95rem;
  flex: 1;
}
.bio-like-row .action-buttons-right {
  margin: 0;
  min-width: 110px;
  align-items: center;
  height: auto;
}
.location {
  font-size: 0.9rem;
  color: #888;
}
.bio {
  margin: 0.5rem 0;
  font-size: 0.95rem;
}
.action-buttons {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}
.action-buttons-right {
  display: flex;
  align-items: flex-end;
  margin-top: 0.5rem;
  margin-left: 1.5rem;
  min-width: 110px;
  height: 100%;
}
.btn-like {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  background: linear-gradient(90deg, #3c1650 0%, #901d6a 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(139, 96, 211, 0.10);
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
}
.btn-like:hover {
  filter: brightness(1.08);
  transform: scale(1.11);
  box-shadow: 0 6px 18px 0 rgba(60, 22, 80, 0.35), 0 1.5px 6px 0 rgba(144, 29, 106, 0.18);
}
.profile-main {
  display: flex;
  gap: 2rem;
}
.left-column, .right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(144, 29, 106, 0.10);
  border: 1.5px solid transparent;
  transition: border 0.2s, box-shadow 0.35s cubic-bezier(0.4,0.2,0.2,1), transform 0.35s cubic-bezier(0.4,0.2,0.2,1);
}
.card:hover {
  border: 1.5px solid #901d6a;
  box-shadow: 0 10px 32px rgba(144, 29, 106, 0.18);
  transform: translateY(-7px) scale(1.025);
}
.portfolio-item {
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.item-subtitle {
  font-size: 0.85rem;
  color: #666;
}
.edu-list, .work-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.edu-list li {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}
.work-experience .work-list.lined li {
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}
.job-entry {
  font-size: 0.9rem;
  line-height: 1.4;
}
.dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 0.5rem;
}
.purple { background: #3c1650; }
.red { background: #e85a5a; }
.gray { background: #999; }
.blue { background: #901d6a; }
.pink { background: #e041a0; }
.green { background: #5cc99a; }
@media (max-width: 700px) {
  .edit-profile-btn {
    position: static;
    margin-bottom: 1rem;
    width: 100%;
    justify-content: center;
  }
  .user-info {
    flex-direction: column;
    align-items: stretch;
  }
  .action-buttons-right {
    margin-left: 0;
    margin-top: 1rem;
    align-items: flex-start;
    height: auto;
  }
  .bio-like-row {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  .bio-like-row .action-buttons-right {
    margin-top: 0.5rem;
    justify-content: flex-start;
  }
}
</style>
