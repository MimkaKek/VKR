import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PingView from '../views/PingView.vue'
import TestDBView from '../views/TestDBView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ping',
      name: 'ping',
      component: PingView
    },
    {
      path: '/test_db',
      name: 'testDB',
      component: TestDBView
    }
  ]
})

export default router
