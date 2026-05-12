<template>
    <div class="macros-view">
        
        <section class="macros-card">
          <h1 class="macros-title">Buscador de Macronutrientes</h1>
           <p class="macros-subtitle">
        Escribe un alimento para consultar sus macronutrientes de forma rápida y clara.
      </p>
        <div v-if="BusquedaHecha===false" class="busqueda-box" >
          <div class="input-wrapper">
            <input  v-model="foodInput" @input="buscarSugerencias" placeholder="Escribe un alimento"  class="input-buscador"/>
            <ul v-if="sugerencias.length > 0" class="dropdown">
                <li  v-for="item in sugerencias":key="item" @click="seleccionarSugerencia(item)" class="dropdown-item">
                {{item}}
                </li>
            </ul>
            </div>
        
            <button @click="buscar"class="btn-buscar">Buscar</button>
        </div>

        <div v-if="BusquedaHecha===true" class="resultado-card">
  
            <FoodMacros v-if="alimentoBuscado" :food="alimentoBuscado" />

        </div>

        <div v-if="BusquedaHecha">
            <button @click="nuevaBusqueda" class="btn-nuevaBusqueda">Nueva Búsqueda</button>
        </div>

        
     </section>
    </div>

</template>

<script setup lang="ts">
    import FoodMacros from'../components/FoodMacros.vue'
    import{ref} from 'vue'
    import {useRouter, useRoute} from 'vue-router'

    const route= useRoute()
    const router = useRouter();



    const foodInput=ref('')
    const food = route.params.food
    const alimentoBuscado=ref('')
    const BusquedaHecha=ref(false)
    
    const sugerencias= ref<string[]>([])
    interface tipos{
      tipos: string[]
    }

    const respuestaTipos=ref<tipos|null>(null)
    async function buscarSugerencias(){
      const texto = foodInput.value.trim()
        if (!texto) {
          sugerencias.value = []
          return
        }else{

        const respuestaTipos = await fetch(`https://proyectoapi.orangeground-d354b437.swedencentral.azurecontainerapps.io/tipos?food=${encodeURIComponent(texto)}`)
        const data = await respuestaTipos.json()
        sugerencias.value=data.tipos
        }
        
    }
    function buscar() {
        const valor = foodInput.value.trim()
        if (!valor) return

        alimentoBuscado.value = valor
        BusquedaHecha.value=true
        
        
}

    function seleccionarSugerencia(item: string) {
      foodInput.value = item
      sugerencias.value = []
    }

    function nuevaBusqueda() {
        foodInput.value=''
      alimentoBuscado.value=''
      sugerencias.value=[]
      BusquedaHecha.value=false
      route
    }
</script>

<style scoped>
.input-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px;
}

.input-buscador {
  width: 100%;
  padding: 14px 18px;
  border-radius: 14px;
  border: none;
  outline: none;
  font-size: 1rem;
  box-sizing: border-box;
}


.lista {
  max-width: 700px;
  margin:  20px ;
  text-align: center;
  color:azure;
  font-size: 1.1rem;
  line-height: 1.5;
}
.dropdown {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 100%;
  margin: 0;
  padding: 6px 0;
  list-style: none;
  background: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  max-height: 220px;
  overflow-y: auto;
  z-index: 1000;
}
.dropdown-item {
  padding: 10px 12px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}
.busqueda-box {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
}
.input-buscador {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  

}
.macros-view {
  min-height: calc(100vh - 140px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 60px 20px;
}

.macros-card {
  width: 100%;
  max-width: 760px;
  background: rgba(255, 255, 255, 0.14);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: 24px;
  padding: 36px 32px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.22);
  text-align: center;
}

.macros-title {
  margin: 0 0 12px;
  font-size: 2.2rem;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
}

.macros-subtitle {
  margin: 0 0 28px;
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.92);
}

.busqueda-box {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.input-buscador {
  width: 100%;
  max-width: 420px;
  padding: 14px 18px;
  border-radius: 14px;
  border: none;
  outline: none;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.95);
  color: #1f2a44;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.btn-nuevaBusqueda {
  padding: 14px 24px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  background: #ff6b57;
  color: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-nuevaBusqueda:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 87, 0.35);
}
.btn-buscar {
  padding: 14px 24px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 700;
  background: #2b2827;
  color: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-buscar:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(65, 54, 51, 0.35);
}


.dropdown {
  width: 100%;
  max-width: 420px;
  margin: 0 auto 20px;
  padding: 8px 0;
  list-style: none;
  background: white;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16);
  text-align: left;
  overflow: hidden;
}

.dropdown-item {
  padding: 12px 16px;
  cursor: pointer;
  color: #1f2a44;
  transition: background 0.2s ease;
}

.dropdown-item:hover {
  background: #f4f6fb;
}

.resultado-card {
  margin-top: 28px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 18px;
  padding: 24px;
  text-align: left;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
}

</style>