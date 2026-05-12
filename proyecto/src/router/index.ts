import { createRouter, createWebHistory } from 'vue-router';
import FoodMatch from '../components/FoodMatch.vue'
import HomeView from '@/views/HomeView.vue';
import FoodMacros from'../components/FoodMacros.vue'
import MacrosView from '../views/MacrosView.vue'

const router = createRouter({
  history: createWebHistory(), // El "historial" del navegador
  routes: [
    {
    path: '/',
    name: 'home',
    component: HomeView // El componente de bienvenida
    },
    {
      path: '/buscador',
      name: 'Buscador',
      component: FoodMatch,
    },
    {
      path: '/macros',
      name: 'Macros',
      component: MacrosView,
    },
    {
      path: '/macros/:food',
      name: 'MacrosId',
      component: MacrosView,

    }
  ],
});

export default router;