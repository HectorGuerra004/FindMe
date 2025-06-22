<template>
    <div class="profile-page-background">
        <div class="profile-container">
        <aside class="sidebar">
            <div class="profile-intro card">
            <img :src="user.avatar" alt="User Avatar" class="profile-avatar">
            <h1 class="profile-name">{{ user.name }}</h1>
            <p class="profile-location">{{ user.location }}</p>
            <p class="profile-bio-short">{{ user.bioShort }}</p>
            </div>

            <div class="portfolio card">
            <h2 class="card-title">Portfolio</h2>
            <div class="project-demo">
                <div class="project-thumbnail">
                <span class="play-icon">&#9658;</span>
                </div>
                <div class="project-info">
                <p class="project-title">Project Demo</p>
                <p class="project-details">Website / App</p>
                </div>
            </div>
            <div class="like-buttons">
                <button class="btn btn-like-purple">● Like</button>
                <button class="btn btn-like-pink">● Like</button>
            </div>
            </div>

            <div class="education-summary card">
            <h2 class="card-title">Education</h2>
            <p>{{ user.educationSummary }}</p>
            </div>
        </aside>

        <main class="main-content">
            <header class="main-header">
            <div class="logo">
                <span class="logo-icon">#</span> Findme
            </div>
            <nav class="main-nav">
                <a href="#" class="nav-link">Contact</a>
                <a href="#" class="nav-link">Gstats</a>
                <a href="#" class="nav-link">Doolc</a>
                <button class="btn btn-primary">Dony Ine</button>
            </nav>
            </header>

            <div class="details-card">
            <div class="bio-full">
                <p>{{ user.bioFull }}</p>
                <span class="arrow-icon">&gt;</span>
            </div>
            
            <div class="contact-info">
                <div>
                <span class="icon">[t]</span> Duinde
                <span class="icon">[m]</span> {{ user.phone }}
                <span class="icon">[e]</span> {{ user.email }}
                </div>
                <div>
                <button class="btn btn-secondary">PONECF</button>
                <button class="btn btn-icon">?</button>
                </div>
            </div>

            <div class="pills-section">
                <span class="pill">+755-12 455</span>
                <span class="pill">Jane 123 457</span>
                <span class="pill">ecnnalid</span>
                <button class="btn btn-action">Pylce</button>
            </div>

            <div class="cards-container">
                <div class="info-card">
                <h3 class="card-title">Skills</h3>
                <ul>
                    <li v-for="skill in user.skills" :key="skill.name" :class="`level-${skill.level}`">
                    <span class="skill-dot"></span>
                    {{ skill.name }} - <span class="skill-level">{{ skill.level }}</span>
                    </li>
                </ul>
                </div>

                <div class="info-card">
                <h3 class="card-title">Work Experience</h3>
                <ul>
                    <li v-for="job in user.experience" :key="job.id">
                    <span class="icon">[w]</span> {{ job.id }}
                    </li>
                </ul>
                </div>
            </div>
            </div>
        </main>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UserProfile',
    data() {
        return {
            user: {
                name: 'Jane Doe',
                location: 'San Francisco, CA',
                avatar: 'https://i.pravatar.cc/150?img=1', // Placeholder avatar
                bioShort: 'Experienced software engineer looking for new opportunities.',
                educationSummary: 'Jame. Endgrigiel Dicom',
                bioFull: 'Experienced software engineer passionate about building innovative solutions.',
                phone: '+1 555 13-4567',
                email: 'jane.doe@example.com',
                skills: [
                    { name: 'Python', level: 'advanced' },
                    { name: 'Javascript', level: 'intermediate' },
                    { name: 'Typescript', level: 'intermediate' },
                    { name: 'UX Design', level: 'basic' },
                    { name: 'Ando-icn', level: 'basic' },
                ],
                experience: [
                    { id: '07 132 1730', company: 'TechCorp' },
                    { id: '07 132 3310', company: 'Innovate LLC' },
                    { id: '07 167 1430', company: 'DevSolutions' },
                    { id: 'G2 132 2330', company: 'Web Services Inc.' },
                ],
            },
        };
    },
};
</script>

<style scoped>
/* ======================================= */
/* =           VARIABLES Y GLOBALES      = */
/* ======================================= */
:root {
    --bg-color: #f4f5fa;
    --card-bg: #ffffff;
    --text-primary: #333;
    --text-secondary: #777;
    --primary-purple: #8e44ad;
    --light-purple: #d8c8e1;
    --accent-pink: #e91e63;
    --accent-purple-light: #a974ff;
    --border-color: #e0e0e0;
    --shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    --border-radius-m: 12px;
    --border-radius-l: 20px;
}

/* ======================================= */
/* =           LAYOUT PRINCIPAL          = */
/* ======================================= */
.profile-page-background {
    background-color: var(--bg-color);
    font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 2rem;
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    min-height: 100vh;
}

.profile-container {
    display: flex;
    gap: 2rem;
    width: 100%;
    max-width: 1200px;
}

.sidebar {
    flex: 0 0 280px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.card {
    background-color: var(--card-bg);
    border-radius: var(--border-radius-l);
    padding: 1.5rem;
    box-shadow: var(--shadow);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* ======================================= */
/* =        COMPONENTES DE SIDEBAR       = */
/* ======================================= */
.profile-intro {
    text-align: center;
}

.profile-avatar {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 1rem;
    border: 4px solid var(--card-bg);
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.profile-name {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
}

.profile-location {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-top: 0.25rem;
}

.profile-bio-short {
    margin-top: 1rem;
    font-size: 0.9rem;
}

.portfolio .project-demo {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.project-thumbnail {
    width: 60px;
    height: 60px;
    background-color: #333;
    border-radius: var(--border-radius-m);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 1.5rem;
}

.project-title {
    font-weight: 600;
}
.project-details {
    color: var(--text-secondary);
    font-size: 0.8rem;
}

.like-buttons {
    display: flex;
    gap: 0.5rem;
}

.btn {
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}
</style>