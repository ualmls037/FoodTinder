<template>
    <div>
        <h3>Macronutrientes de {{ props.food }}</h3>
    </div>
    <div v-if="Macronutrientes">
        <ul>
            <li>Energía: {{ Macronutrientes.macros.energia }}</li>
            <li>Proteínas: {{ Macronutrientes.macros.proteinas }}</li>
            <li>Carbohidratos: {{ Macronutrientes.macros.carbohidratos }}</li>
            <li>Grasas: {{ Macronutrientes.macros.grasas }}</li>
        </ul>
    </div>

 
</template>

<script setup lang="ts">
import {ref,onMounted} from 'vue'

const props = defineProps<{
  food: string
}>()

interface result {
    energia: number
    proteinas:number
    grasas:number
    carbohidratos:number

}
interface ResultadoAPI{
    alimento: string
    macros: result

}
const Macronutrientes= ref<ResultadoAPI|null>(null)

onMounted(async () =>{ //Para inciar lógica cuando aparece la componente en pantalla
    const macrosAPI= await fetch(`https://proyectoapi.orangeground-d354b437.swedencentral.azurecontainerapps.io/macros?food=${encodeURIComponent(props.food)}`)
    const data: ResultadoAPI= await macrosAPI.json()
    Macronutrientes.value=data
})

</script>

