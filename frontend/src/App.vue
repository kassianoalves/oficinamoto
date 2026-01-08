<template>
  <div id="app" class="app-container">
    <nav class="navbar">
      <div class="logo">
        <h1>🏍️ Oficina Moto</h1>
      </div>
      <ul class="nav-menu">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/clientes">Clientes</router-link></li>
        <li><router-link to="/motos">Motos</router-link></li>
        <li><router-link to="/manutencoes">Manutenções</router-link></li>
      </ul>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f5f5f5;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.logo h1 {
  font-size: 1.8rem;
  font-weight: 700;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 2rem;
}

.nav-menu a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  background: rgba(255, 255, 255, 0.2);
}

.main-content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-menu {
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .logo h1 {
    font-size: 1.4rem;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
