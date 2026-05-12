<template>
    <div >
        <!-- <h2>Recetas</h2> -->
    
     <div v-if="cargando " class="estado-recetas">
        <p>Generando recetas...</p>
    </div>

    <div v-else-if="mensajeError " class="estado-recetas error-recetas">
      <p>{{ mensajeError }}</p>
    </div>

    <div  v-else-if="Recetas" class="lista-recetas-wrapper">


        <ul v-if="props.foodsBase.length>0" class="lista-recetas" >
        <li v-for="item in Recetas.recetas":key="item.titulo" class="item-receta" >
        {{ item.titulo}}
        <button @click="receta_seleccionada=item; close=false " class="btn-ver-receta">Ver receta</button>
        </li>
        </ul>

    </div>

      <div v-if="receta_seleccionada&& close===false" class="overlay-receta">
        <div class="carta-receta">
        <button @click="cerrar()"class="cerrar">X</button>
            <h3 class="titulo-receta">{{ receta_seleccionada.titulo }}</h3>
            <pre class="contenido-receta">{{ receta_seleccionada.cuerpo }}</pre>
      </div>
      </div>

  </div>
  

 
</template>

<script setup lang="ts">
import {ref,onMounted} from 'vue'

const props = defineProps<{
    foodsBase: string[]
    recomendacion: string[]
}>()

const receta_seleccionada= ref<recetas|null>(null)

interface recetas {
    titulo: string
    cuerpo:string    
}
interface ResultadoAPI{
    recetas:recetas[]

}

const cargando =ref(false)
const Recetas= ref<ResultadoAPI|null>(null)
const foods=ref<string[]>([])
const close=ref(false)
const mensaje=ref('Generando recetas...')
const mensajeError=ref('')

function cerrar(){
    close.value=true
}


onMounted(async () => {
  cargando.value = true
  mensajeError.value = ''
  Recetas.value = null

  try {
    const partesFoods = props.foodsBase.map(
      item => `foods=${encodeURIComponent(item)}`
    )
    const query1 = partesFoods.join('&')

    const partesRec = props.recomendacion.map(
      item => `recomendacion=${encodeURIComponent(item)}`
    )
    const query2 = partesRec.join('&')

    const recetasAPI = await fetch(
      `https://proyectoapi.orangeground-d354b437.swedencentral.azurecontainerapps.io/recetas?${query1}&${query2}`
    )

    if (!recetasAPI.ok) {
      const errorData = await recetasAPI.json()
      throw new Error(
        errorData.detail || 'Imposible generar recetas en este momento. Inténtalo más tarde.'
      )
    }

    const data = await recetasAPI.json()
    Recetas.value = data
  } catch (error: any) {
    mensajeError.value =
      'Imposible generar recetas en este momento. Inténtalo más tarde.'
  } finally {
    cargando.value = false
  }
})



</script>

<style scoped>

.carta-recetap {
display:flex;
  margin-top: 20px;
  padding: 20px;
  width: 350px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.overlay-receta {
  position: fixed;
  inset: 0;
  z-index: 5000;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  box-sizing: border-box;

}

.estado-recetas {
  text-align: center;
  padding: 20px;
  color: white;
  font-weight: 600;
}
.lista-recetas-wrapper {
  margin-top: 20px;
}

.lista-recetas {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.item-receta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.92);
}

.btn-ver-receta {
  border: none;
  border-radius: 10px;
  padding: 10px 16px;
  background: #1f2a44;
  color: white;
  cursor: pointer;
}
.btn-ver-receta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(65, 54, 51, 0.35);
}
.carta-receta {
  position: relative;
  width: 100%;
  max-width: 950px;
  max-height: 88vh;
  overflow-y: auto;
  padding: 32px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.3);
}
.cerrar {
  position: absolute;
  top: 16px;
  right: 16px;
  border: none;
  background: #ef4444;
  color: white;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
}
.titulo-receta {
  margin: 0 0 20px 0;
  color: #080808;
  font-size: 2rem;
}
.contenido-receta {
  background: #f7f8fb;
  border-radius: 18px;
  padding: 22px;

}

.contenido-receta pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-family: inherit;
  line-height: 1.7;
  color: #2d3748;
}

</style>


