// initial state

import axios from 'axios'

const state = () => ({
    sid: null,
    role: 0,
    status: false
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
    },
    logout: (state) => {
        state.status = false;
        state.sid    = null;
        state.role   = 0;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}