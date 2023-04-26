<script>
import { mapGetters } from 'vuex';
import Button from '@/components/common/Button.vue';
import InputText from '../common/InputText.vue';
import auth from '../../store/modules/auth';

export default {
    components: {
        Button,
        InputText
    },
    data() {
        return {
            loginTitle: "Авторизация",
            regTitle: "Register",
            formName: "",
            formPass: "",
        }
    },
    methods: {
        Login() {
            this.$store.dispatch('auth/login', {name: this.formName, pass: this.formPass, mail: ""}).then(() => {
                if (this.$store.getters['auth/status']) {
                    this.$router.push('/projects');
                }
                else {
                    alert("Авторизация не удалась!");
                    this.formName = "";
                    this.formPass = "";
                }
            });
        },
        ToRegister() {
            this.$router.push('/register');
        }
    },
    watch: {
        option: {}
    },
    computed: {},
    mounted() {
        this.$store.commit('auth/logout');
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            <div class="form">
                {{ this.loginTitle }}
                <InputText v-model="formName" :placeholder="'Имя или почта'"/>
                <InputText v-model="formPass" :placeholder="'Пароль'"/>
            </div>
            <div class="form-btns">
                <Button class="log-btn first" :title="'Регистрация'" :func="ToRegister"></Button>
                <Button class="log-btn" :title="'Войти'" :func="Login"></Button>
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

.form-btns {
    padding-left: 10px;
    padding-right: 10px;
    display: flex;
    flex-direction: column;
}
.box .log-btn.first {
    margin-right: 5px;
}

</style>