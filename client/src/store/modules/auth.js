// initial state
import cookie from 'vue-cookies'
import axios from 'axios'

const state = () => ({
    sid: cookie.isKey("sid") ? cookie.get("sid") : null,
    role: cookie.isKey("role") ? cookie.get("role") : null,
    status: cookie.isKey("status") ? cookie.get("status") : false
})
  
// getters
const getters = {
    sid: state => {
        return state.sid;
    },
    role: state => {
        return state.role;
    },
    status: state => {
        return state.status;
    }
}

// actions
const actions = {
    register: ({ commit }, user) => {
        const path = 'http://localhost:8000/user';

        const parameters = {
            name: user.name,
            mail: user.mail,
            pass: user.pass
        };

        const headers = {
            'Content-Type': 'application/json'
        };

        return axios.put(path, null, {params: parameters, headers: headers})
                    .then((response) => {
                        if (response.data.status == 0) {
                            console.debug("Registered succesfuly!");
                            commit('login', response.data.data);
                        }
                        else {
                            console.debug("Register failed!");
                            console.debug("Description: " + response.data.description);
                        }
                    })
                    .catch((error) => {
                        console.error(error);
                    });
    },
    login: ({ commit }, user) => {
        const path = 'http://localhost:8000/user';

        const parameters = {
            name: user.name,
            mail: user.mail,
            pass: user.pass
        };

        const headers = {
            'Content-Type': 'application/json'
        };

        return axios.post(path, null, {params: parameters, headers: headers})
                    .then((response) => {
                        if (response.data.status == 0) {
                            console.debug("Logged succesfuly!");
                            console.log(user);
                            var uData = response.data.data;
                            commit('login', uData);
                        }
                        else {
                            console.debug("Login failed!");
                            console.debug("Description: " + response.data.description);
                        }
                    })
                    .catch((error) => {
                        console.error(error);
                    });
    },
    logout: ({ commit }) => {
        commit('logout');
    }
}

// mutations
const mutations = {
    login: (state, uData) => {
        state.status = true;
        state.sid    = uData.sid;
        state.role   = uData.role;

        cookie.set("sid", uData.sid, "7d");
        cookie.set("role", uData.role, "7d");
        cookie.set("status", true, "7d");
    },
    logout: (state) => {
        state.status = false;
        state.sid    = null;
        state.role   = null;
        
        cookie.remove("sid");
        cookie.remove("role");
        cookie.remove("status");
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}