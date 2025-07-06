<template>
  <div class="login-container">
    <h2>Iniciar sesión</h2>
    <form>
      <input type="text" placeholder="Usuario" />
      <input type="password" placeholder="Contraseña" />
      <button type="submit">Entrar</button>
    </form>
    <div class="register-link">
      ¿No tienes cuenta? <router-link to="/register">Regístrate aquí</router-link>
    </div>
  </div>
</template>

<script setup>
// Aquí puedes agregar la lógica de login si lo deseas
</script>

<style scoped>
.login-container {
  max-width: 350px;
  margin: 100px auto;
  padding: 2rem;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-align: center;
}
.login-container h2 {
  margin-bottom: 1.5rem;
}
.login-container input {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}
.login-container button {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
}
.register-link {
  margin-top: 1.5rem;
  font-size: 0.95rem;
}
.register-link a {
  color: #1a1a3c;
  text-decoration: underline;
}
</style>
