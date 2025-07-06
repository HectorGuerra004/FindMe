<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router' // Importa useRouter
import axios from 'axios' // Importa axios

const sidebarVisible = ref(true)
const isMobile = ref(false)
const username = ref("John Doe")

const router = useRouter() // Inicializa useRouter

// Icono dinámico para el botón
const sidebarIcon = computed(() => {
    if (isMobile.value) {
        return sidebarVisible.value ? 'close' : 'menu'
    }
    return sidebarVisible.value ? 'arrow_back' : 'menu'
})

const emit = defineEmits(['state-change'])

const emitState = () => {
    emit('state-change', {
        visible: sidebarVisible.value,
        isMobile: isMobile.value
    })
}

const toggleSidebar = () => {
    sidebarVisible.value = !sidebarVisible.value
    emitState()
}

const closeSidebar = () => {
    sidebarVisible.value = false
    emitState()
}

const closeIfMobile = () => {
    if (isMobile.value) {
        closeSidebar()
    }
}

const checkMobile = () => {
    const wasMobile = isMobile.value
    isMobile.value = window.innerWidth < 768

    if (!wasMobile && isMobile.value) {
        sidebarVisible.value = false
    } else if (wasMobile && !isMobile.value) {
        sidebarVisible.value = true
    }

    emitState()
}

// *** Nueva función logout ***
const logout = async () => {
    try {
        // 1. Cierra la barra lateral (si es móvil) inmediatamente para una mejor UX
        closeIfMobile();

        // 2. Realiza la llamada POST a tu backend
        const response = await axios.post('/logout');

        // 3. Maneja la respuesta del backend
        console.log(response.data.message); // Debería mostrar "Sesión cerrada"

        // 4. Limpia cualquier dato de sesión del lado del cliente (ej. token en localStorage)
        // Esto es crucial para asegurar que la sesión se invalide completamente en el frontend.
        localStorage.removeItem('userToken'); // Si guardas un token JWT aquí
        // localStorage.removeItem('userRole'); // Cualquier otro dato de sesión

        // 5. Redirige al usuario a la página de inicio de sesión o a la página principal
        // Asegúrate de que '/login' sea la ruta correcta para tu página de inicio de sesión
        router.push('/login');

    } catch (error) {
        // Manejo de errores si la solicitud falla
        console.error('Error al cerrar sesión:', error);
        alert('Hubo un problema al cerrar sesión. Por favor, inténtalo de nuevo.');
        // Incluso si falla la llamada al backend, a menudo querrás redirigir
        // para evitar que el usuario se quede "logueado" en el frontend sin una sesión backend válida.
        router.push('/login');
    }
}

onMounted(() => {
    checkMobile()
    window.addEventListener('resize', checkMobile)
    emitState()
})
</script>

<template>


    <aside :class="['sidebar', { 'visible': sidebarVisible }]">
        <div class="sidebar-header">
            <h2 class="titulo">Find<Span>Me</Span>
            </h2>
            <button class="close-button" @click="closeSidebar" v-if="isMobile">
                <span class="material-icons">close</span>
            </button>
        </div>

        <div class="menu">
            <router-link to="/" class="button" @click="closeIfMobile">
                <span class="material-icons">home</span>
                <span class="text">Inicio</span>
            </router-link>
            <router-link to="/profile" class="button" @click="closeIfMobile">
                <span class="material-icons">account_circle</span>
                <span class="text">Perfil de usuario</span>
            </router-link>
            <router-link to="/configuration" class="button" @click="closeIfMobile">
                <span class="material-icons">settings</span>
                <span class="text">Configuración</span>
            </router-link>
        </div>
        <div class="menu-bottom">
            <router-link to="/" class="button" @click="logout">
                <span class="material-icons">logout</span>
                <span class="text">Logout</span>
            </router-link>
        </div>
    </aside>
    <header class="header" :class="{ 'desktop-sidebar-visible': !isMobile && sidebarVisible }">
        <div class="header-left">
            <button class="toggle-button" @click="toggleSidebar">
                <span class="material-icons">{{ sidebarIcon }}</span>
            </button>
        </div>
        <div class="header-right">
            <router-link to="/login" class="button-nav user-info">

                <span class="text">Login</span>
            </router-link>
            <router-link to="/register" class="button-nav user-info">
                <!-- <span class="material-icons">account_circle</span> -->
                <span class="text">Register</span>
            </router-link>
        </div>
    </header>
</template>

<style scoped>
/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
    height: 60px;
    background-color: white;
    color: black;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    /* box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); */
    transition: left 0.3s ease;

}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.header-right {
    display: flex;
    align-items: center;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    margin-right: 5px;
    background-color: white;
}

.toggle-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem;
}

.logo {
    font-size: 1.5rem;
    margin: 0;
}

.titulo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1a1a3c;
}

.titulo span {
    color: #b04cc8;
}

/* Sidebar */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 250px;
    background-color: #f0f1f6;
    color: white;
    z-index: 1001;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    /* transition: transform 0.3s ease; */
}

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    /* border-bottom: 1px solid #2c3e50; */
    color: black;
}

.close-button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    display: block;
}

/* Menú */
.menu,
.menu-bottom {
    padding: 1rem;
}

.menu-bottom {
    margin-top: auto;
    padding-bottom: 2rem;
}

.button {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: black;
    text-decoration: none;
    border-radius: 25px;
    margin-bottom: 0.5rem;
    transition: background-color 0.2s;
    width: 100%;
    background-color: white;
}

.button:hover {
    background-color: #2c3e50;
}

.button.router-link-exact-active {
    background-color: #3498db;
}

.button-nav {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    text-decoration: none;
    color: white;

    border-radius: 20px;
    margin-bottom: 0.5rem;
    transition: background-color 0.2s;
    width: 100%;
    background-color: #2c3e50;
}

.button-nav:hover {
    background-color: #3c4145;
}

/* .button-nav.router-link-exact-active {
    background-color: #3498db;
} */

.material-icons {
    margin-right: 1rem;
    color: black;

}

/* Responsive: Móvil */
@media (max-width: 767px) {
    .sidebar {
        transform: translateX(-100%);
        width: 85%;
        max-width: 300px;
    }

    .sidebar.visible {
        transform: translateX(0);
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
        z-index: 1001;
        /* Mayor que el header (1000) */

    }

    .sidebar.visible+.main-content::after {
        content: '';
        position: fixed;
        top: 60px;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 998;
    }

    .user-info span:first-child {
        display: none;
    }
}

/* Responsive: Desktop */
@media (min-width: 768px) {
    .sidebar:not(.visible) {
        transform: translateX(-100%);
    }

    .sidebar.visible {
        transform: translateX(0);
    }

    .close-button {
        display: none;
    }

    .toggle-button .material-icons {
        transition: transform 0.3s ease;
    }


    .header.desktop-sidebar-visible {
        left: 250px;
        /* Igual al ancho del sidebar */
        width: calc(100% - 250px);
    }
}
</style>