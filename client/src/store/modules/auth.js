// initial state

import axios from 'axios'

const state = () => ({
    name: "",
    mail: "",
    pass: "",
    status: false
})
  
// getters
const getters = {
    name: state => {
        return state.name;
    },
    mail: state => {
        return state.mail;
    },
    pass: state => {
        return state.pass;
    },
    status: state => {
        return state.status;
    }
}

// actions
const actions = {
    login: (state, payload) => {
        const path = 'http://localhost:8000/user';

        const config = {
            method: 'get',
            url: 'http://webcode.me',
            headers: { 'User-Agent': 'Axios - console app' }
        }

        const data = {
            user: {
                name: payload.name,
                mail: payload.mail,
                pass: payload.pass
            }
        };
        const strData = JSON.stringify(data);
        const headers = {
            'Content-Type': 'application/json'
        };
        axios
            .get(path, {headers: headers, data: strData})
            .then((response) => {
                if (response.data.status == 0) {
                    console.debug("Logged succesfuly!");
                    
                    state.status = true;
                    state.mail   = payload.mail;
                    state.name   = payload.name;
                    state.pass   = payload.pass;
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
    logout: (state, payload) => {
        state.status = false;
        state.mail   = "";
        state.name   = "";
        state.pass   = "";
    }
}

// mutations
const mutations = {
    login: (state, payload) => {
        state.status = true;
        state.mail   = payload.mail;
        state.name   = payload.name;
        state.pass   = payload.pass;
    },
    logout: (state, payload) => {
        state.status = false;
        state.mail   = "";
        state.name   = "";
        state.pass   = "";
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}