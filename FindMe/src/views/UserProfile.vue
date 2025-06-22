<template>
  <div class="app-container">
    <aside class="sidebar">
      <h1 class="logo">find<span>me</span></h1>
      <nav>
        <ul>
          <li><button><img :src="userImage" alt="User" class="avatar" /> Home</button></li>
          <li><button><i class="icon-profile"></i> Profile</button></li>
          <li><button><i class="icon-search"></i> Search</button></li>
          <li><button class="active"><i class="icon-id"></i> 907764</button></li>
          <li><button><i class="icon-search"></i> Search</button></li>
          <li><button><i class="icon-connection"></i> Connections</button></li>
          <li><button><i class="icon-settings"></i> Settings</button></li>
        </ul>
      </nav>
      <div class="footer">
        <button>View Provisions</button>
      </div>
    </aside>
    <main class="main-content">
      <header class="main-header">
        <h2>Find professionals</h2>
        <div class="search-bar">
          <input type="text" placeholder="Find Professionals" />
          <button class="icon-button"><i class="icon-search"></i></button>
        </div>
        <div class="filter-bar">
          <button class="location-button">Home</button>
          <input type="text" placeholder="At Design Corporation" />
          <button class="filter-button">Dpr</button>
          <button class="filter-button">0078a</button>
        </div>
        <div class="user-menu">
          <i class="icon-user"></i>
          <span>Contact</span>
          <button class="outgoing-button">Outgoing</button>
        </div>
      </header>
      <section class="cards-grid">
        <div v-for="user in users" :key="user.id" class="card">
          <img :src="user.image" class="card-avatar" />
          <div class="card-info">
            <h3>{{ user.name }}</h3>
            <p>{{ user.title }}</p>
            <p class="location">{{ user.location }}</p>
          </div>
          <div class="card-actions">
            <button class="connect-button">Connect</button>
            <button class="connect-button">Connect</button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const userImage = 'https://via.placeholder.com/40';

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
]);
</script>

<style scoped>
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
