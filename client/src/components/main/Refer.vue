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
        }
    },
    methods: {

        async useLink() {
            const path = 'http://localhost:8000/link/' + this.$route.params.shareLink;
            
            var sid = this.$store.getters['auth/sid'];
            const parameters = {
                sid: sid
            };

            console.log("USE LINK FUNC");
            const headers = {
                'Content-Type': 'application/json'
            };
            await axios.patch(path, null, {params: parameters, headers: headers})
                        .then((response) => {
                            if (response.data.status != 0) {
                                console.error("Use project link failed!");
                                console.error("Description: " + response.data.description);
                                return null;
                            }
                            alert("Ссылка успешно использована!");
                            this.$router.push('/projects');
                        })
                        .catch((error) => {
                            console.error(error);
                            alert("Что-то пошло не так...");
                            this.$router.push('/projects');
                        });
        }
    },
    mounted() {
        this.useLink();
    }
}

</script>

<template>
    <div class="main"></div>
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

</style>