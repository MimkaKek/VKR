import { createRouter, createWebHistory } from 'vue-router'
import LoginView        from '../views/LoginView.vue'
import RegisterView     from '../views/RegisterView.vue'
import ProjectsView     from '../views/ProjectsView.vue'
import PubProjectsView  from '../views/PubProjectsView.vue'
import TemplatesView    from '../views/TemplatesView.vue'
import RolesView        from '../views/RolesView.vue'
import EditorView       from '../views/EditorView.vue'
import InfoView         from '../views/InfoView.vue'
import SettingsView     from '../views/SettingsView.vue'
import CreateView       from '../views/CreateView.vue'
import ReferView        from '../views/ReferView.vue'
import ShareView        from '../views/ShareView.vue'

import store from '../store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/',                       redirect: '/projects'                         },
    { path: '/login',                  name: 'login',    component: LoginView        },
    { path: '/register',               name: 'register', component: RegisterView     },
    { path: '/public',                 name: 'public',   component: PubProjectsView  },
    { path: '/projects',               name: 'projects', component: ProjectsView     },
    { path: '/templates',              name: 'templates',component: TemplatesView    },
    { path: '/roles',                  name: 'roles',    component: RolesView        },
    { path: '/project/edit/:pid',      name: 'editor',   component: EditorView       },
    { path: '/project/info/:pid',      name: 'info',     component: InfoView         },
    { path: '/project/settings/:pid',  name: 'settings', component: SettingsView     },
    { path: '/project/create',         name: 'create',   component: CreateView       },
    { path: '/project/share/:pid',     name: 'share',    component: ShareView        },
    { path: '/project/ref/:shareLink', name: 'useRefer', component: ReferView        },
  ]
})

router.beforeEach(async (to) => {
  const publicPages  = ['/login', '/register'];
  const authRequired = !publicPages.includes(to.path);
  const auth         = store.getters['auth/status'];
  
  if (authRequired && !auth) {
      return '/login';
  }
});

export default router
