<script>
import { mapGetters } from 'vuex';
import Button from '../common/Button.vue'
import InputText from '../common/InputText.vue';

export default {
    components: {
        Button,
        InputText
    },
    data() {
        return {
            loginTitle: "Login",
            regTitle: "Register",
            formMail: "",
            formName: "",
            formPass: "",
            formConfPass: "",
        }
    },
    methods: {

    },
    watch: {
    option: {
    }
    },
    computed: {
    ...mapGetters(["option"]),
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            Регистрация
            <InputText v-model="formName" :placeholder="'Почта'"/>
            <InputText v-model="formName" :placeholder="'Имя'"/>
            <InputText v-model="formPass" :placeholder="'Пароль'"/>
            <InputText v-model="formConfPass" :placeholder="'Подтвердите пароль'"/>
            <Button class="log-btn" title="Зарегистрироваться" func=""></Button>
        </div>
    </div>
</template>

<style scoped>

.log-btn {
    margin-top: 10px;
}

.main {
    display: flex;
    min-height: 92.8%;
    background-color: rgb(41, 41, 41);
    align-items: center;
    justify-content: center;
}

.box {
    font-size: 20px;
    display: flex;
    background-color: rgb(55, 55, 55);
    flex: 0 1 20%;
    padding: 10px;
    border-radius: 10px;
    border: 2px solid rgb(88 88 88);
    flex-direction: column;
    align-items: center;
}

.box input.first {
    margin-top: 10px;
}

.box span {
    font-size: 12px;
}
 
.link {
    color: rgb(60, 113, 192)
}

</style>