import { createApp } from 'vue'
import VueCookies from 'vue-cookies'
import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

app.use(VueCookies)
app.use(router)
app.use(store)

app.mount('#app')
