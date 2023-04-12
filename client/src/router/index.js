import { createRouter, createWebHistory } from 'vue-router'
import EditorView   from '../views/EditorView.vue'
import LoginView    from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import store from '../store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',              redirect: '/projects'                     },
    { path: '/login',         name: 'login',    component: LoginView    },
    { path: '/register',      name: 'register', component: RegisterView },
    { path: '/projects',      name: 'projects', component: ProjectsView },
    { path: '/project/:sid',  name: 'editor',   component: EditorView   },
    { path: '/refer/:sid',    name: 'useRefer', component: ProjectsView }
  ]
})

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages  = ['/login'];
  const authRequired = !publicPages.includes(to.path);
  const auth         = store.getters['auth/status'];

  if (authRequired && !auth) {
      return '/login';
  }
});

export default router
