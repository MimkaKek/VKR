import { createRouter, createWebHistory } from 'vue-router'
import EditorView   from '../views/EditorView.vue'
import LoginView    from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProjectsView from '../views/ProjectsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login',         name: 'login',    component: LoginView    },
    { path: '/register',      name: 'register', component: RegisterView },
    { path: '/projects',      name: 'projects', component: ProjectsView },
    { path: '/project/:sid',  name: 'editor',   component: EditorView   }
  ]
})

export default router
