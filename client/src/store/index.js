import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
  state: {
      name: "",
      mail: "",
      pass: "",
      logged: false
  },
  getters: {
    nameGet(state) {
      return state.name;
    },
    mailGet(state) {
      return state.mail;
    },
    passGet(state) {
      return state.pass;
    }
  },
  mutations: {
    nameSet (state, payload) {
      state.name = payload.name;
    },
    mailSet (state, payload) {
      state.mail = payload.mail;
    },
    passSet (state, payload) {
      state.pass = payload.pass;
    }
  }
})

export default store