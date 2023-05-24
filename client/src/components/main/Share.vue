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
            link: null,
            tUpdate: "Обновить"
        }
    },
    methods: {

        async updLink() {
            const path = 'http://localhost:8000/link/' + this.$route.params.pid;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            const headers = {
                'Content-Type': 'application/json'
            };

            await axios.put(path, null, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Update project link failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.link = location.host + "/project/ref/" + response.data.data;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        },

        async getLink() {
            const path = 'http://localhost:8000/link/' + this.$route.params.pid;
            
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
                                console.error("Get project link failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }

                            this.link = location.host + "/project/ref/" + response.data.data;
                        })
                        .catch((error) => {
                            console.error(error);
                        });
        }
    },
    mounted() {
        this.getLink();
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            <div>
                <InputText v-model="this.link" :locked="true" :placeholder="'Ссылка...'"/>
            </div>
            <div class="save-btn">
                <Button :func="this.updLink">
                    {{ this.tUpdate }}
                </Button>
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
    font-size: 20px;
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