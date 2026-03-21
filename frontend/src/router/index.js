import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/MainView.vue'
import PublicView from '../views/PublicView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainView
    },
    {
      path: '/view/:id',
      name: 'public-view',
      component: PublicView
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

export default router
