<template>
  <section >
    <div class="capa">
      <div class="contenido">
    <h1>Food Tinder</h1>
    <h2>Encuentra combinaciones de alimentos de forma inteligente.</h2>
          <p>Food Tinder analiza alimentos y te sugiere parejas compatibles según su composición, 
          además de mostrar sus macronutrientes y diferentes recetas para que explores opciones de manera fácil y visual.
          </p>
    <button @click="empezarApp" class="btn-empezar">Empezar</button>
  
    
          </div>
      </div>
    </section>

</template>

<script setup lang="ts">
import {useRouter} from 'vue-router'

const router= useRouter()

async function empezarApp(){
  router.push('/buscador')
   const conectar = await fetch(`https://proyectoapi.orangeground-d354b437.swedencentral.azurecontainerapps.io/`)
  
}

</script>

<style scoped>


.capa {
  min-height: 100vh;
  width: 100%;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  box-sizing: border-box;
}

.contenido {
  max-width: 800px;
  color: white;
  text-align: center;
}

.contenido h1 {
  font-size: 4rem;
  margin-bottom: 16px;
}

.contenido h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.contenido p {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 24px;
}
.btn-empezar {
  padding: 14px 24px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  background: #68412e;
  color: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-empezar:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(65, 54, 51, 0.35);
}
</style>