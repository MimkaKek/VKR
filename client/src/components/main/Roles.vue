<script>
import Button from '../common/Button.vue';
import InputText from '../common/InputText.vue';
import axios from 'axios';

export default {
    components: {
        Button,
        InputText
    },
    data() {
        return {
            users: {"user1": 1, "user2": 2, "user3": 3},
            columns: ["Имя", "Роль"],
            roles: {"Учащийся": 3, "Преподаватель": 2, "Администратор": 1},
            search_usr: "",
            search_role: 3
        }
    },
    methods: {
        async getUsers() {
            const path = 'http://localhost:8000/users';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            return axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get users failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.users = response.data.data;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        async updateRoleWrapper(user, role) {

            if (user == "" || role < 1 || role > 3) {
                console.error("Fields not filled!");
                return null;
            }

            await this.updateRole(user, role);
            await this.getUsers();
        },
        async updateRole(user, role) {

            const path = 'http://localhost:8000/user';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };
            
            const data = {
                'data': {
                    "name": user,
                    "role": role
                }
            }

            return axios.patch(path, data, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Update role failed!");
                                console.error("Description: " + response.data.description);
                                this.getUsers();
                                return null;
                            }
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        }
    },
    mounted() {
        this.getUsers();
    }
}

</script>

<template>
    <div class="main">
        <div class="box search">
            <div class="ml-5 w-320">
                <InputText v-model="this.search_usr" :placeholder="'Имя пользователя...'"/>
            </div>
            <div class="ml-5 w-220">
                <select v-model="this.search_role">
                    <option v-for="(r_value, r_name) in this.roles" :value="r_value"> 
                        {{ r_name }}
                    </option>
                </select>
            </div>
            <div class="ml-5 w-220">
                <Button :func="this.updateRoleWrapper" :fArgs="[this.search_usr, this.search_role]">
                    Обновить
                </Button>
            </div>
        </div>
        <div class="box">
            <table>
                <tr>
                    <th v-for="headItem in this.columns">
                        {{ headItem }}
                    </th>
                </tr>
                <template v-for="(role, user) in this.users">
                    <tr>
                        <td>
                            {{ user }}
                        </td>
                        <td class="roles">
                            <select v-model="this.users[user]" @change="this.updateRole(user, this.users[user])">
                                <option v-for="(r_value, r_name) in this.roles" :value="r_value"> 
                                    {{ r_name }}
                                </option>
                            </select>
                        </td>
                    </tr>
                </template>
            </table>
        </div>
    </div>
</template>

<style scoped>
.main {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 100%;
    padding-top: 65px;
    display: flex;
    background-color: rgb(41, 41, 41);
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

select {
    width: 100%;
    height: 40px;
    background-color: rgb(60, 60, 60);
    border: 1px solid rgb(90, 90, 90);
    color: rgb(226, 226, 226);
    font-size: 20px;
    text-align: center;
    outline: none;
}

select:hover {
    width: 100%;
    height: 40px;
    background-color: rgb(92, 92, 92);
    border: 1px solid rgb(90, 90, 90);
    transition: border 0.25s linear 0s;
    font-size: 20px;
    text-align: center;
}

.box {
    margin: 10px;
    width: 800px;
    font-size: 20px;
    background-color: rgb(55, 55, 55);
    padding: 10px;
    border-radius: 10px;
    border: 2px solid rgb(88 88 88);
}

.box.search {
    margin: 10px;
    width: 800px;
    font-size: 20px;
    background-color: rgb(55, 55, 55);
    padding: 4px;
    border-radius: 5px;
    border: 2px solid rgb(88 88 88);
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  margin: 0px;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

td, th {
  border: 1px solid #969696;
  text-align: center; 
  padding: 8px;
}

td.roles {
    padding: 0px;
}

tr {
  background-color: rgb(65, 65, 65);
}

.search {
    display: flex;
    align-items: center;
}

.search input {
    border-radius: 0%;
    padding: 10px 20px;
}

.search button {
    padding: 8px;
}
.ml-5 {
    margin-left: 5px;
}

.w-320 {
    width: 320px;
}

.w-220 {
    width: 220px;
}

</style>