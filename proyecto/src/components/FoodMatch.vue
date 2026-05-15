<template>
  <div class="pantalla-foodmatch">
    <div class="buscador" >
      <div class="caja-explicacion">
          <p class="descripcion-app">
      Escribe uno o más alimentos para descubrir sus mejores combinaciones,
      consultar los macronutrientes de cada opción y generar distintas recetas
      a partir de la selección de alimentos recomendados.
      
          </p>
    </div>
      <div v-if="!busquedaHecha" class="bloque-input">
        <input  v-model="foodInput" @input="buscarSugerencias" placeholder="Escribe un alimento" class="input-buscador" />
        <ul v-if="sugerencias.length > 0" class="dropdown">
          <li  v-for="item in sugerencias":key="item" @click="seleccionarSugerencia(item)" class="dropdown-item">
            {{item}}
          </li>
        </ul>
        <button @click="añadir" class="btn-añadir">Añadir</button>

      </div >
        <ul v-if="foods.length > 0 " class="lista-alimentos">
          
            <li v-for="(item,indice) in foods" :key="item" class="item-alimento">
            {{ item }}
            <button v-if="!busquedaHecha" @click="eliminar(indice)" class="btn-eliminar">Eliminar</button>
            </li>

        </ul>
    <div >
      
        <div>
          <button v-if="foods.length>0  && busquedaHecha==false " @click="buscar" class="btn-buscar">Buscar</button>
          <div v-if="cargando" class="texto">Buscando recomendaciones...</div>
          <p v-if="busquedaHecha" class="mensaje-error">{{mensaje}}</p>
        </div>

        <div v-if="busquedaHecha==true">
          <button @click="nuevaBusqueda" class="btn-nuevaBusqueda">Nueva Búsqueda</button>
        </div>
            
        </div>
        

    
    </div   v-if="busquedaHecha" class="panel-recomendaciones">
        <ul  v-if="resultado" class="lista-recomendaciones"> 
          <h3 v-if="resultado.recomendaciones.length!==0"class="titulo-recomendaciones">Recomendaciones</h3>
          
            <!-- //Etiqueta típica para pintar elementos uno debajo de otro -->
            <li v-for="item in resultado.recomendaciones" :key="item.food" class="fila-recomendacion">
              
                <span class="nombre-recomendacion">{{ item.food }}</span>
                <div class="acciones-recomendacion">
                  <div class="bloque-botones">
                  <button @click="verMacros(item.food)" class="btn-macros">Macros</button>
                  <button @click="selec=item.food;añadirRecomendacion();alimentoseleccionado=''" class="btn-receta">Añadir a la lista</button>
                </div>
                </div>
              </li>
      </ul>


    <div class="panel-seleccionados" v-if="alimentoseleccionado1.length>0">
      <h3 class="titulo-seleccionados"> Alimentos seleccionados para generar recetas </h3>
      <ul  class="lista-seleccionados-receta">
        
          <li v-for="(item,indice) in alimentoseleccionado1" :key="item" class="chip-receta">
            {{ item }}
            <botton @click="eliminarRecomendacion(indice)" class="btn-quitar-chip">✕</botton>

          </li>

        </ul>
        <button v-if="!recetasGeneradas" @click="generarRecetas" class="btn-generar-recetas">Recetas</button>
        <button v-else @click="generarRecetas" class="btn-generar-recetas">Generar nuevas recetas</button>
            <div v-if="mostrarRecetas" class="bloque-recetas">
          <FoodRecetas :key="claveRecetas":foodsBase="foods":recomendacion="alimentoseleccionado2"  />
      </div>
    </div>
         </div>


    
      
  
      
   

    <div v-if="alimentoseleccionado" class="overlay-macros" >
      <div class="modal-macros">
        <button class="cerrar-macros" @click="cerrarMacros">✕</button>
        <FoodMacros v-if="alimentoseleccionado":key="alimentoseleccionado":food="alimentoseleccionado"/>
        </div>
      </div>

    
</template>

<script setup lang="ts">
    import { ref} from 'vue'
    import FoodMacros from './FoodMacros.vue'
    import FoodRecetas from './FoodRecetas.vue'

    interface recomendacion1{
        food:string
    }
    interface ResultadoAPI {
        recomendaciones: recomendacion1[]
    }
    const alimentoseleccionado= ref('')
    const alimentoseleccionado1=ref<string[]>([])
    const alimentoseleccionado2=ref<string[]>([])
    const selec=ref('')
    // Al llamar al alimneto seleccionado de dos formas diferentes 
    // conseguimos que no salagna los macros y las recetas a la vez cuando se le da a uno de los botones
  
    const foodInput=ref('')

    const foods=ref<string[]>([])
 
    const resultado = ref<ResultadoAPI|null>(null)

    const busquedaHecha= ref(false)
    const cargando =ref(false)
    const mostrarRecetas=ref(false)
    const pulsado=ref(false)
    const claveRecetas=ref(0)
    const recetasGeneradas=ref(false)
    const mostrarMacros=ref(false)

  


    function cerrarMacros() {
      mostrarMacros.value = false
      alimentoseleccionado.value = ''
    }

    
    function añadirRecomendacion(){
      const valor=selec.value.trim()

      if(!valor) return

      if(!alimentoseleccionado1.value.includes(valor)){
        alimentoseleccionado1.value.push(valor)
        
      }
      mostrarRecetas.value=false
      recetasGeneradas.value=false
      claveRecetas.value++

    }

    function eliminarRecomendacion(indice:number){
      alimentoseleccionado1.value.splice(indice, 1)
      alimentoseleccionado2.value.splice(indice, 1)
      mostrarRecetas.value=false
      recetasGeneradas.value=false
    }
    function verMacros(food: string) {
      alimentoseleccionado.value = food

      alimentoseleccionado1.value = []
      alimentoseleccionado2.value = []
      mostrarRecetas.value = false
      recetasGeneradas.value = false
      claveRecetas.value++
}
    function generarRecetas() {
      cargando.value=true
      if (alimentoseleccionado1.value.length === 0) return

      alimentoseleccionado2.value = [...alimentoseleccionado1.value]
      mostrarRecetas.value = true
      claveRecetas.value++
      alimentoseleccionado.value = ''
      recetasGeneradas.value=true
      cargando.value=false
    }

    function añadir(){
        const valor=foodInput.value.trim()
        if(valor ==='') return

        foods.value.push(valor)
        foodInput.value=''
        sugerencias.value=[]
        mostrarRecetas.value=false
    }

    const mensaje=ref('')
    const errorMensaje=ref('')

    async function buscar(){
      errorMensaje.value=''
  
        cargando.value=true
        alimentoseleccionado.value=''
        resultado.value = null
        mensaje.value = ''
        const partes = foods.value.map(item => `foods=${encodeURIComponent(item)}`)
        const query = partes.join('&')
    
        const respuestaAPI= await fetch(`https://proyectoapi.orangeground-d354b437.swedencentral.azurecontainerapps.io/recomendar?${query}`)
         
        const data =await respuestaAPI.json()
        
        if (!respuestaAPI.ok) {
          mensaje.value = data.detail 
          resultado.value = null
          cargando.value=false
          busquedaHecha.value=true
          return
        }
        resultado.value=data
        if (data.recomendaciones.length === 0) {
          mensaje.value = 'No se han encontrado recomendaciones para esos alimentos.'
          busquedaHecha.value=false
          cargando.value=false
        }else{
          mensaje.value=''
        }
      


      
      

      cargando.value=false
      busquedaHecha.value=true

    }
  
    function nuevaBusqueda() {
      foods.value = []
      alimentoseleccionado1.value=[]
      alimentoseleccionado.value=''
      resultado.value=null
      mensaje.value==''
      busquedaHecha.value=false
      cargando.value=false
      alimentoseleccionado2.value=[]



    }

    function eliminar(indice:number){
      foods.value.splice(indice, 1)
      mostrarRecetas.value=true

    }

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

    function seleccionarSugerencia(item: string) {
      foodInput.value = item
      sugerencias.value = []
    }
    

 

   



</script>

<style scoped>
.modal-macros {
  position: relative;
  width: 100%;
  max-width: 850px;
  max-height: 85vh;
  overflow-y: auto;
  padding: 32px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.3);
}
.overlay-macros {
  position: fixed;
  inset: 0;
  z-index: 5000;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 24px;
  box-sizing: border-box;
}
.cerrar-macros {
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
.mensaje-error {
  max-width: 700px;
  margin: 24px auto 0 auto;
  padding: 16px 22px;
  border-radius: 16px;

  color: white;
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  /* box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); */
  /* backdrop-filter: blur(8px); */
}
.texto{
  color:honeydew
}

.pantalla-foodmatch {
  min-height: 100vh;
  width: 100%;

  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  box-sizing: border-box;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 60px;
  padding: 40px;
}

.lista {
  max-width: 700px;
  margin:  20px ;
  text-align: center;
  color:azure;
  font-size: 1.1rem;
  line-height: 1.5;
}

.left-panel {
  max-width: 520px;
}

.left-panel h1 {
  font-size: 56px;
  margin: 0 0 20px 0;
}

.left-panel h2 {
  font-size: 30px;
  font-weight: 500;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

.left-panel p {
  font-size: 18px;
  line-height: 1.6;
  color: #333;
}

.right-panel {
  min-width: 420px;
}

.search-row {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-row input {
  flex: 1;
  padding: 12px 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.search-row button,
.search-button,
.result-actions button {
  padding: 10px 14px;
  font-size: 15px;
  border: 1px solid #bbb;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

.search-row button:hover,
.search-button:hover,
.result-actions button:hover {
  background: #f3f3f3;
}

.selected-foods {
  margin: 0 0 20px 0;
  padding-left: 20px;
}

.selected-foods li {
  margin-bottom: 8px;
  font-size: 18px;
}

.search-button {
  margin-bottom: 25px;
}

.results-list {
  margin: 0;
  padding-left: 20px;
}

.results-list li {
  margin-bottom: 14px;
  font-size: 18px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.result-actions {
  display: flex;
  gap: 8px;
}

.macros-box,
.recipes-box {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background: #fafafa;
}

.macros-box h2,
.recipes-box h2 {
  margin-top: 0;
  margin-bottom: 12px;
}

.macros-box ul,
.recipes-box ul {
  padding-left: 20px;
  margin: 0;
}

.macros-box li,
.recipes-box li {
  margin-bottom: 8px;
}

pre {
  white-space: pre-wrap;
  word-break: break-word;
}
.receta-texto {
  display:flex;
  white-space: pre-wrap;
  line-height: 1.6;
  font-size: 1.1rem;
}
.carta-receta {
  margin-top: 20px;
  padding: 20px;
  width: 350px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}
.buscador {
  position: relative;
  width: 300px;
}

.input-buscador {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
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

.caja-explicacion {
  max-width: 700px;
  margin: 0 auto 24px auto;
  padding: 22px 28px;
  background: rgba(0, 0, 0, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 18px;
  backdrop-filter: blur(6px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
}

.descripcion-app {
  margin: 0;
  color: white;
  font-size: 1.15rem;
  line-height: 1.6;
  text-align: center;
}
.bloque-input {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 18px;
  margin-bottom: 18px;
}

.lista-alimentos {
  list-style: none;
  padding: 0;
  margin: 0 auto 20px auto;
  width: 100%;
  max-width: 420px;
}

.item-alimento {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.88);
  border-radius: 12px;
  color: #1f2a44;
}

.btn-eliminar {
  border: none;
  background: #e74c3c;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
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
.btn-añadir {
  padding: 14px 24px;
  border-radius: 14px;
  background: #8d9168;
  color: white;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.btn-añadir:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 184, 99, 0.35);
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
.panel-recomendaciones {
  max-width: 900px;
  margin: 30px auto 0 auto;
  padding: 24px;
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  backdrop-filter: blur(8px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
}

.titulo-recomendaciones {
  margin: 0 0 18px 0;
  text-align: center;
  color: white;
  font-size: 1.5rem;
}

.lista-recomendaciones {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.fila-recomendacion {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 14px;
}

.nombre-recomendacion {
  font-size: 1.15rem;
  font-weight: 600;
  color: #1f2a44;
}

.acciones-recomendacion {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.btn-macros,
.btn-receta {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
  font-size: 0.95rem;
}

.btn-macros {
  background: #1f2a44;
  color: white;
}

.btn-receta {
  background: #8d9168;
  color: white;
}
.btn-receta:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(151, 194, 154, 0.35);
}
.btn-macros:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(134, 112, 110, 0.35);
  
}
.bloque-botones {
  width: 190px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex-shrink: 0;
}
.panel-seleccionados {
  max-width: 900px;
  margin: 24px auto 0 auto;
  padding: 22px;
  background: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  backdrop-filter: blur(8px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
}

.titulo-seleccionados {
  margin: 0 0 16px 0;
  text-align: center;
  color: white;
  font-size: 1.3rem;
}

.lista-seleccionados-receta {
  list-style: none;
  margin: 0 0 20px 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
}

.chip-receta {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.92);
  color: #1f2a44;
  padding: 10px 14px;
  border-radius: 999px;
  font-size: 1rem;
  font-weight: 600;
}

.btn-quitar-chip {
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 50%;
  background: #e74c3c;
  color: white;
  cursor: pointer;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 0;
  line-height: 1;
  font-size: 16px;
}
.btn-quitar-chip:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 87, 0.35);
}

.btn-generar-recetas {
  display: block;
  margin: 0 auto;
  border: none;
  border-radius: 12px;
  padding: 12px 22px;
  background: #1d222c;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
}
.btn-generar-recetas:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(173, 161, 159, 0.35);
}
.columna-recetas {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 620px;
}

.bloque-recetas {
  width: 100%;
}

@media (max-width: 1000px) {
  .container {
    flex-direction: column;
  }

  .right-panel {
    width: 100%;
    min-width: 0;
  }
}
</style>