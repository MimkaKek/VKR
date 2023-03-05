<script>
import { mapGetters } from 'vuex';
import Button from '@/components/common/Button.vue';
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
            formName: "",
            formPass: "",
        }
    },
    methods: {
        Login() {
            return 'Foo'
        },
        ToRegister() {
            this.$router.push({ name: "register" })
        }
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
            <div class="form">
                Вход
                <InputText v-model="formName" :placeholder="'Имя или почта'"/>
                <InputText v-model="formPass" :placeholder="'Пароль'"/>
            </div>
            <div>
                <Button class="log-btn first" :title="'Регистрация'" :func="ToRegister"></Button>
                <Button class="log-btn" :title="'Войти'" :func="Login"></Button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.main {
    display: flex;
    min-height: 92.8%;
    background-color: rgb(41, 41, 41);
    align-items: center;
    justify-content: center;
}

.form {
    display: flex;
    flex: 0 1 20%;
    flex-direction: column;
    align-items: center;
}

.box {
    font-size: 20px;
    background-color: rgb(55, 55, 55);
    padding: 10px;
    border-radius: 10px;
    border: 2px solid rgb(88 88 88);
}

.box input.first {
    margin-top: 10px;
}

.log-btn {
    display: inline;
    margin-top: 10px;
}

.box .log-btn.first {
    margin-right: 5px;
}

</style>