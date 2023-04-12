import { createStore } from 'vuex'
import authModule from './modules/auth'

// Create a new store instance.
const store = createStore({
  modules: {
    auth: authModule
  }
})

export default store