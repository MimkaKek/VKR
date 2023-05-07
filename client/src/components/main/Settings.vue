<script>
import Button from '../common/Button.vue';
import InputText from '../common/InputText.vue';
import axios from 'axios';

export default {
    props: {
        locked: {
            type: Boolean,
            default: false
        },
        create: {
            type: Boolean,
            default: false
        },
        type: {
            type: String,
            default: "project"
        }
    },
    components: {
        Button,
        InputText
    },
    data() {
        return {
            projectMeta: {
                name: "",
                description: "",
                isPublic: false,
                isTemplate: false,
            },
            role: 3,
            templates: {},
            selected: ""
        }
    },
    methods: {
        changePublic() {
            this.projectMeta.isPublic = this.projectMeta.isPublic ? false : true;
            return null;
        },
        changeTemplate() {
            this.projectMeta.isTemplate = this.projectMeta.isTemplate ? false : true;
            return null;
        },
        getProjectData() {
            const path = 'http://localhost:8000/project/' + this.$route.params.pid;
            
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
                                console.error("Get project data failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.projectMeta = response.data.data.meta;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        setProjectData() {
            const path = 'http://localhost:8000/project/' + this.$route.params.pid;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };
            
            var data = {"data": this.projectMeta};
            
            axios.patch(path, data, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get project data failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            
                            this.$router.back();
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        createNewProject() {
            const path = 'http://localhost:8000/projects';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };
            
            var data = {"data": {"meta": this.projectMeta, "tid": this.selected}};

            axios.put(path, data, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Create new project failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            
                            this.$router.back();
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },
        saveProjectMeta() {
            this.setProjectData();
        },
        doNothing() {},
        async getTemplates() {
            const path = 'http://localhost:8000/templates_all';
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            await axios.get(path, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Get project data failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            console.log(response.data.data);
                            this.templates = response.data.data;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        }
    },
    mounted() {
        this.getTemplates();
        this.role = this.$store.getters["auth/role"];
        
        if (!this.create) {
            this.getProjectData();
        }
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            <div>
                <InputText v-model="this.projectMeta.name" :locked="this.locked" :placeholder="'Название...'"/>
            </div>
            <div class="area">
                <InputText v-model="this.projectMeta.description" :locked="this.locked" :textarea="true" :placeholder="'Описание...'"/>
            </div>
            <div>
                <div class="menu-text">
                    <div class="filler">
                        Доступ
                    </div>
                    <div v-if="this.role < 3" class="filler">
                        Тип проекта
                    </div>
                    <div v-if="this.create" class="filler">
                        Шаблон
                    </div>
                </div>
                <div class="menu-btn">
                    <div class="filler">
                        <Button :locked="this.locked" :func="this.changePublic">
                            {{ this.projectMeta.isPublic ? 'Публичный' : 'Закрытый' }}
                        </Button>
                    </div>
                    <div v-if="this.role < 3" class="filler">
                        <Button :locked="this.locked" :func="this.changeTemplate">
                            {{ this.projectMeta.isTemplate ? 'Шаблон' : 'Проект' }}
                        </Button>
                    </div>
                    <div v-if="this.create" class="filler">
                        <select v-model="this.selected">
                            <option disabled value="">...</option>
                            <option v-for="(key, value) in this.templates" :value="value">
                                {{ key }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="!this.locked" class="save-btn">
                    <Button v-if="this.create" :func="this.createNewProject">
                        Создать
                    </Button>
                    <Button v-else :func="this.saveProjectMeta">
                        Сохранить
                    </Button>
                </div>
            </div>
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
}

.menu-btn {
    display: flex;
    margin-top: 10px;
    width: 100%;
    height: 100%;
}

.locked {
    margin-top: 20px;
}
.save-btn {
    margin-top: 10px;
    margin-left: 5px;
    margin-right: 5px;
}
.filler {
    width: 100%;
    margin-left: 5px;
    margin-right: 5px;
}

.filler select {
    width: 100%;
    height: 100%;
    background-color: rgb(92, 92, 92);
    outline: none;
    border: 2px solid rgb(90, 90, 90);
    transition: border 0.25s linear 0s;
    color: rgb(233, 233, 233);
}

.filler select:hover {
    width: 100%;
    height: 100%;
    background-color: rgb(92, 92, 92);
    outline: none;
    border: 2px solid rgb(90, 90, 90);
    transition: border 0.25s linear 0s;
    color: rgb(233, 233, 233);
}

.subfiller {
    width: 20%;
}
.menu-text {
    display: flex;
    margin-top: 20px;
    text-align: center;
    width: 100%;
    height: 100%;
}

.area {
    height: 230px;
}
.box {
    width: 800px;
    font-size: 20px;
    background-color: rgb(55, 55, 55);
    padding: 10px;
    border-radius: 10px;
    border: 2px solid rgb(88 88 88);
}

</style>