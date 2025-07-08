<template>
  <div class="app-container">
    <SideBar @state-change="handleSidebarState" />
    <main :class="['main-content', { shifted: sidebarVisible && !isMobile }]">
      <div class="profile-page">

        <section class="profile-header" v-if="profileData">
          <div class="user-info">
            <div class="avatar-wrapper" style="position: relative; display: inline-block;">
              <img class="avatar" :src="userAvatar || 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png'"
                alt="User Avatar" />
              <div class="avatar-overlay" @click="onEditAvatar">
                <span class="avatar-pencil">✎</span>
              </div>
            </div>
            <div class="details details-row">
              <h2>{{ profileData?.nombre || 'Usuario sin nombre' }} {{ profileData?.apellido || '' }}</h2>
              <p class="location">{{ profileData?.ubicacion || 'Ubicación no disponible' }}</p>
              <div class="bio-like-row">
                <p class="bio">Numero de Contacto: {{ profileData?.telefono || 'Este usuario no ha escrito su biografía.' }}</p>
                <div class="action-buttons action-buttons-right">
                  <button v-if="!isOwnProfile && profileData.user" :class="['btn-like', { 'liked': isLiked }]"
                    @click="onLikeProfile">
                    {{ isLiked ? 'Quitar Like' : '👍 Like' }}
                  </button>
                  <span v-if="profileData.likes_count !== undefined" class="likes-count">
                    {{ profileData.likes_count }} Likes
                  </span>
                </div>
              </div>
            </div>
          </div>
          <router-link v-if="isOwnProfile" to="/completeProfile" class="edit-profile-btn" title="Completar perfil">
            ✎ Completar perfil
          </router-link>
        </section>

        <div class="card" v-if="profileData?.sobre_mi">
          <h3>Sobre Mí</h3>
          <p>{{ profileData.sobre_mi }}</p>
        </div>

        <section class="profile-main" v-if="!loading && profileData">
          <div class="left-column">
            <div class="card">
              <h3>Habilidades</h3>
              <ul v-if="profileData?.habilidades?.length">
                <li v-for="(skill, index) in profileData.habilidades" :key="skill.id || index">
                  {{ skill.nombre_skill }} — {{ skill.nivel }}
                </li>
              </ul>
              <p v-else>No se han agregado habilidades.</p>
            </div>
          </div>

          <div class="right-column">
            <div class="card">
              <h3>Educación</h3>
              <ul class="edu-list" v-if="profileData?.educacion?.length">
                <li v-for="(edu, index) in profileData.educacion" :key="edu.id || index">
                  <span class="dot purple"></span>
                  {{ edu.titulo }} en {{ edu.campo_estudio }} — {{ edu.institucion }}
                </li>
              </ul>
              <p v-else>No se ha agregado información educativa.</p>
            </div>

            <div class="card work-experience">
              <h3>Experiencia Laboral</h3>
              <ul class="work-list lined" v-if="profileData?.experiencia?.length">
                <li v-for="(job, index) in profileData.experiencia" :key="index">
                  <div class="job-entry">
                    <strong>{{ job.empresa }}</strong> — {{ job.puesto }}<br />
                    {{ job.ubicacion_exp }}<br />
                    {{ formatDate(job.inicio_exp) }} — {{ job.fin_exp ? formatDate(job.fin_exp) : 'Actualidad' }}
                  </div>
                </li>
              </ul>
              <p v-else>No se ha agregado experiencia laboral.</p>
            </div>
          </div>
        </section>

        <p v-if="loading">Cargando perfil...</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import SideBar from '@/components/sideBar/SideBar.vue'
import { useRoute } from 'vue-router';
import useProfile from '@/services/profiles.js';
import likesService from '@/services/likes.js'; // Importa el servicio de likes

const route = useRoute();
const { getProfileData, getProfileById } = useProfile();

const sidebarVisible = ref(true)
const isMobile = ref(false)
const userAvatar = ref('')

const profileData = ref(null);
const loading = ref(false);
const error = ref(null);
const isOwnProfile = ref(false);
const currentUserId = ref(null);
const isLiked = ref(false);

const handleSidebarState = (state) => {
  sidebarVisible.value = state.visible
  isMobile.value = state.isMobile
}

const getCurrentUserIdFromStorage = () => {
  const storedUser = localStorage.getItem('user')
  if (!storedUser) return null
  try {
    const parsed = JSON.parse(storedUser)
    return parsed.id // Este es el ID del usuario logueado
  } catch (e) {
    console.error('Error al parsear usuario del localStorage:', e)
    return null
  }
}

const fetchCurrentUserId = () => {
  currentUserId.value = getCurrentUserIdFromStorage()
}

const loadProfileData = async () => {
  loading.value = true;
  error.value = null;

  try {
    const userIdParam = route.params.id; // Este es el ID de la URL
    fetchCurrentUserId(); // Obtiene el ID del usuario logueado desde localStorage

    console.log('ID de la URL (userIdParam):', userIdParam);
    console.log('ID del usuario logueado (currentUserId.value):', currentUserId.value);

    const resolvedId = parseInt(userIdParam); // ID numérico de la URL
    const actualId = currentUserId.value; // ID numérico del usuario logueado

    // Importante: La comparación inicial con el ID de la URL
    isOwnProfile.value = resolvedId === actualId;

    // Carga los datos del perfil
    profileData.value = isOwnProfile.value
      ? await getProfileData() // Obtiene el perfil del usuario logueado
      : await getProfileById(resolvedId); // Obtiene el perfil por ID de la URL

    console.log('Datos del perfil cargados (profileData):', profileData.value);

    // --- CAMBIOS CLAVE PARA OBTENER EL ID CORRECTO DEL PERFIL ---
    // Usamos profileData.value.user como el ID real del perfil para las operaciones de likes
    const profileIdToUse = profileData.value?.user;

    console.log('ID del perfil cargado (profileIdToUse - de profileData.user):', profileIdToUse);

    // Re-evaluar isOwnProfile usando el ID real del perfil desde el backend
    // Esto es crucial para asegurar que la bandera sea correcta.
    isOwnProfile.value = profileIdToUse === actualId;
    console.log('¿Es el perfil propio (isOwnProfile) después de la carga y re-evaluación?:', isOwnProfile.value);

    // Asigna la imagen de perfil
    if (profileData.value?.img_profile) {
      userAvatar.value = profileData.value.img_profile;
    } else {
      userAvatar.value = 'https://cdn-icons-png.flaticon.com/512/1144/1144760.png';
    }

    // Lógica para verificar el estado del like
    // Solo si NO es el perfil propio y si tenemos un ID de perfil válido (profileIdToUse)
    if (!isOwnProfile.value && profileIdToUse) { // <-- Condición actualizada
      const likeStatus = await likesService.checkIfLiked(profileIdToUse); // <-- Usa profileIdToUse
      isLiked.value = likeStatus.is_liked;
      console.log('Estado de like (isLiked):', isLiked.value);
    } else {
      isLiked.value = false;
      console.log('No se verificó el like (perfil propio o sin ID de perfil válido). isLiked:', isLiked.value);
    }

  } catch (err) {
    error.value = 'Error cargando perfil del usuario';
    console.error('Detalle del error al cargar perfil:', err);
    isLiked.value = false; // Reinicia el estado del like en caso de error
  } finally {
    loading.value = false;
  }
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const options = { year: 'numeric', month: 'short' };
  return new Date(dateStr).toLocaleDateString('es-ES', options);
};

onMounted(() => {
  fetchCurrentUserId();
  if (route.params.id) {
    loadProfileData();
  }
});

watch(() => route.params.id, (newId) => {
  if (newId) loadProfileData();
});

const onEditAvatar = () => {
  console.log('Editar avatar');
};

const onLikeProfile = async () => {
  const profileIdToSend = profileData.value?.user;

  if (!profileIdToSend) {
    console.warn('No se puede procesar el like, el ID del perfil no está disponible.');
    alert('No se pudo procesar tu acción. Inténtalo de nuevo más tarde.');
    return;
  }

  try {
    const response = await likesService.toggleLike(profileIdToSend);
    isLiked.value = !isLiked.value;

    // ¡CONFIRMA ESTE BLOQUE DE CÓDIGO!
    if (profileData.value && profileData.value.likes_count !== undefined) {
        if (isLiked.value) { // Si acabamos de dar like
            profileData.value.likes_count++;
        } else { // Si acabamos de quitar el like
            profileData.value.likes_count--;
        }
    }

    console.log('Operación de like exitosa:', response.detail || response);

    if (response.detail && response.detail.includes('eliminado')) {
        alert('¡Me gusta eliminado!');
    } else {
        alert('¡Me gusta agregado!');
    }

  } catch (err) {
    console.error('Error al procesar el like:', err.response?.data || err.message);
    alert('Hubo un error al procesar tu "me gusta".');
  }
};
</script>

<style scoped>
/* Estilos que ya tenías */
.error {
  color: red;
  font-weight: bold;
  padding: 1rem;
}

.profile-page {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  background-color: #e1e4e9;
  min-height: 100vh;
  border-radius: 25px;
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
  text-decoration: none;
  position: absolute;
  top: 1.5rem;
  right: 2rem;
  z-index: 2;
  background: linear-gradient(135deg, #03016b 0%, #534bed 100%);
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
  background: linear-gradient(135deg, #03016b 0%, #534bed 100%);
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
  /* align-items: center; */
  height: auto;
}
.action-buttons-right {
  display: flex; /* Para alinear el botón y el texto */
  align-items: center; 
  gap: 10px; /* Espacio entre los elementos */
  /* ... otros estilos que ya tuvieras */
}

.likes-count {
  background: linear-gradient(135deg, #03016b 0%, #534bed 100%);
  font-size: 0.9rem;
  color: #fff;
  font-weight: bold;
  white-space: nowrap; /* Evita saltos de línea */
  padding: 0.5rem 1rem;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(139, 96, 211, 0.10);
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s, filter 0.2s;
  
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

/* CAMBIOS CLAVE AQUÍ: Estilos del botón de Like/Unlike */
.btn-like {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  background: linear-gradient(135deg, #03016b 0%, #534bed 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(139, 96, 211, 0.10);
  transition: background 0.2s, transform 0.2s, box-shadow 0.2s, filter 0.2s;
  /* Añade filter para el hover */
}

.btn-like:hover {
  filter: brightness(1.08);
  transform: scale(1.11);
  box-shadow: 0 6px 18px 0 rgba(60, 22, 80, 0.35), 0 1.5px 6px 0 rgba(144, 29, 106, 0.18);
}

/* Estilo para cuando el perfil ya ha recibido "me gusta" */
.btn-like.liked {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  /* Un color más rojizo para "Quitar Like" */
  color: #fff;
  border: 1px solid #c0392b;
}

.btn-like.liked:hover {
  filter: brightness(1.15);
  /* Aumenta el brillo al pasar el ratón */
}


.profile-main {
  display: flex;
  gap: 2rem;
}

.left-column,
.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.10);
  border: 1.5px solid transparent;
  transition: border 0.2s, box-shadow 0.35s cubic-bezier(0.4, 0.2, 0.2, 1), transform 0.35s cubic-bezier(0.4, 0.2, 0.2, 1);
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

.edu-list,
.work-list {
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

.purple {
  background: #3c1650;
}

.red {
  background: #e85a5a;
}

.gray {
  background: #999;
}

.blue {
  background: #901d6a;
}

.pink {
  background: #e041a0;
}

.green {
  background: #5cc99a;
}

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

@media (max-width: 590px) {
  .profile-main {
    flex-direction: column;
  }

  .left-column,
  .right-column {
    flex: none;
    margin-bottom: 1.5;
  }

  .btn-like {
    margin-bottom: 1.5rem;
  }

  .likes-count{
    margin-bottom: 1rem;
  }
}
</style>