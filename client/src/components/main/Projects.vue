<script>
import Table from '../common/Table.vue';
import Button from '../common/Button.vue';
import axios from 'axios';

export default {
    components: {
        Table,
        Button
    },
    props: {
        type: {
            type: String,
            default: "projects"
        }
    },
    data() {
        return {
            newPID: "",
            btnAdd: "Создать",
            projects: {},
            tHead: ["Название", "Владелец", "Тип", "Создан", "Обновлён", "Действия"],
            tData: [],
            tActions: [],
            isArray: [false, false, false, false, false, true]
        }
    },
    methods: {
        initComponent() {
            if (this.type == "templates") {
                this.tHead   = ["Название", "Владелец", "Тип", "Создан", "Обновлён", "Действия"];
                this.isArray = [false, false, false, false, false, true];
                this.getTemplatesData();
                return;
            }
            else if (this.type == "public") {
                this.tHead   = ["Название", "Описание", "Владелец", "Обновлён", "Действия"];
                this.isArray = [false, false, false, false, false];
                this.getPublicData();
                return;
            }
            
            this.getProjectsData();
            return;
        },
        async getPublic(pid) {
            const path = 'http://localhost:8000/project/' + pid;
            
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
                                console.error("Get project data failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.newPID = response.data.data.pid;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        getProjectsData() {
            const path = 'http://localhost:8000/projects';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get projects failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.projects = response.data.data;

                            for (let pKey in this.projects) {
                                this.projects[pKey].dataKey = this.tData.length;
                                this.tData.push([this.projects[pKey].name,
                                                 this.projects[pKey].owner,
                                                 this.projects[pKey].isPublic ? "Публичный" : "Закрытый",
                                                 this.projects[pKey].created,
                                                 this.projects[pKey].lastUpdated,
                                                 ["Настройки", "Подробнее", "-"]]);
                                this.tActions.push([[this.openProject, [pKey]],
                                                     null,
                                                     null,
                                                     null,
                                                     null,
                                                     [[this.settingProject, [pKey]], [this.infoProject, [pKey]], [this.removeProject, [pKey]]]]);
                            }
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        getTemplatesData() {
            const path = 'http://localhost:8000/templates';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get templates failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.projects = response.data.data;

                            for (let pKey in this.projects) {
                                this.projects[pKey].dataKey = this.tData.length;
                                this.tData.push([this.projects[pKey].name,
                                                 this.projects[pKey].owner,
                                                 this.projects[pKey].isPublic ? "Публичный" : "Закрытый",
                                                 this.projects[pKey].created,
                                                 this.projects[pKey].lastUpdated,
                                                 ["Настройки", "Подробнее", "-"]]);
                                this.tActions.push([[this.openProject, [pKey]],
                                                     null,
                                                     null,
                                                     null,
                                                     null,
                                                     [[this.settingProject, [pKey]], [this.infoProject, [pKey]], [this.removeProject, [pKey]]]]);
                            }
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        getPublicData() {
            const path = 'http://localhost:8000/public_projects';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get public projects failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.projects = response.data.data;

                            for (let pKey in this.projects) {
                                this.projects[pKey].dataKey = this.tData.length;
                                this.projects[pKey].description = this.projects[pKey].description.slice(0, 20) + "..."
                                this.tData.push([this.projects[pKey].name,
                                                 this.projects[pKey].description,
                                                 this.projects[pKey].owner,
                                                 this.projects[pKey].lastUpdated,
                                                 "Подробнее"]);
                                this.tActions.push([[this.openProject, [pKey]],
                                                     null,
                                                     null,
                                                     null,
                                                     [this.infoProject, [pKey]]]);
                            }
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        async openProject(pid) {
            if (this.type == 'public') {
                await this.getPublic(pid);
            }
            else {
                this.newPID = pid;
            }
            this.$router.push('/project/edit/' + this.newPID);
        },
        async removeProject(pid) {
            console.log("RemoveProject Func call with param: " + pid);
            const path = 'http://localhost:8000/project/' + pid;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            await axios.delete(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Remove project failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            this.tData.splice(this.projects[pid].dataKey, 1);
                            this.tActions.splice(this.projects[pid].dataKey, 1);
                            delete this.projects[pid];
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        infoProject(pid) {
            this.$router.push('/project/info/' + pid);
        },
        settingProject(pid) {
            this.$router.push('/project/settings/' + pid);
        },
        createProject() {
            this.$router.push('/project/create');
        }
    },
    watch: {
    },
    computed: {
    },
    mounted() {
        this.initComponent();
    }
}

</script>

<template>
    <div class="main-wrapper">
        <div v-if="this.type != 'public'" class="main-btn-wrapper">
            <Button :func="this.createProject">
                {{ this.btnAdd }}
            </Button>
        </div>
        <div class="main-table-wrapper">
            <Table v-bind:t-head="this.tHead" v-bind:t-data="this.tData" :t-actions="this.tActions" :is-array="this.isArray"></Table>
        </div>
    </div>
</template>

<style>
.main-table-wrapper {
    padding: 10px;
}

.main-btn-wrapper {
    width: 180px;
    padding-left: 10px;
    padding-top: 10px;
}

.main-wrapper {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 100%;
    padding-top: 65px;
    background-color: rgb(41, 41, 41);
}

.main-left {
    width: 20%;
}

.v-divider {
    background-color: rgb(74, 74, 74);
    width: 1px;
    margin-left: 0px;
    margin-right: 5px;
    margin-top: 0px;
    margin-bottom: 0px;
}

.main-right {
    width: 80%;
}

.content-wrapper {
    padding: 20px;
    height: 100%;
}

.func-wrapper {
    margin-top: 0px;
}

.content-disable {
    display: none;
}

.func-item {    
    margin-top: 0px;
    width: 100%;
    height: 50px;
}

.func-btn {
    display: block; 
    height: 100%; 
    width: 100%;
    border: 0px;
    font-size: 20px;
    color: rgb(226, 226, 226);
    background-color: rgb(58, 58, 58);
}

.func-btn:link, .func-btn:visited, .func-btn:focus {
    background: rgb(58, 58, 58);
}

.func-btn:hover {
    background: rgb(65, 65, 65);
}

.func-btn:active {
    background: rgb(63, 63, 63);
}

</style>