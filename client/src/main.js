import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'jquery'
import '@popperjs/core'
import 'bootstrap/dist/js/bootstrap.js'

const app = createApp(App)

app.use(router)

app.mount('#app')
