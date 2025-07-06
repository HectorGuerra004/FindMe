<script setup>
// Aquí puedes agregar la lógica de registro si lo deseas
</script>

<template>
  <div class="register-container">
    <h2>Crear cuenta</h2>
    <form>
      <input type="text" placeholder="Nombre" />
      <input type="text" placeholder="Apellido" />
      <input type="email" placeholder="Correo electrónico" />
      <input type="tel" placeholder="Teléfono" />
      <input type="date" placeholder="Fecha de nacimiento" />
      <input type="text" placeholder="Ubicación (País, Estado, Ciudad)" />
      <input type="password" placeholder="Contraseña" />
      <button type="submit">Registrarse</button>
    </form>
    <div class="login-link">
      ¿Ya tienes cuenta? <router-link to="/">Inicia sesión aquí</router-link>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 2rem;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  text-align: center;
}
.register-container h2 {
  margin-bottom: 1.5rem;
}
.register-container input {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ccc;
}
.register-container button {
  width: 100%;
  padding: 0.5rem;
  border-radius: 8px;
  background: #1a1a3c;
  color: #fff;
  border: none;
  font-weight: bold;
}
.login-link {
  margin-top: 1.5rem;
  font-size: 0.95rem;
}
.login-link a {
  color: #1a1a3c;
  text-decoration: underline;
}
</style>