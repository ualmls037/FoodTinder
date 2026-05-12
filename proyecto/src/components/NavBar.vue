<template>
    <div>
        <nav class="navbar"> 
            <!-- //Etiqueta que sirve para marcar un zona de navegación -->
          <div class="logo-contenedor">
            <img :src="logo" alt="Logo Food Tinder" class="logo-app"/>
          </div>

          <div class="nav-links">
            <RouterLink to="/" class="nav-link" active-class="activo">Inicio</RouterLink>
            <!-- //RouterLink es un enlace intermo de Vue para cambiar de página dentro de la app -->
            <RouterLink to ="/buscador" class="nav-link" active-class="activo">Buscador</RouterLink>
            <RouterLink to ="/macros" class="nav-link" active-class="activo">Macros</RouterLink>
          </div>
        </nav>
    </div>
</template>
<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import logo from '../assets/logo.png'
</script>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 1000;
  margin: 18px auto;
  width: calc(100% - 40px);
  max-width: 1200px;
  padding: 14px 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 22px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
  box-sizing: border-box;
}

.logo-contenedor {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-app {
  width: 150px;
  height: 60px;
  object-fit: contain;
}

.nombre-app {
  color: white;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: 0.3px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 14px;
}
.nav-link{
  text-decoration: none;
  color: rgb(240, 232, 232);
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 14px;
  transition: all 0.25s ease;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
}
.nav-link:hover {
  background: rgba(255, 255, 255, 0.18);
  transform: translateY(-1px);
}
.activo {
  background: rgba(255, 255, 255, 0.92);
  color: #1f2a44;
  text-shadow: none;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.12);
}
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 14px;
    padding: 16px;
  }

  .logo-contenedor {
    justify-content: center;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    padding: 8px 14px;
  }
}
</style>
