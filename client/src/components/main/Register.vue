<script>
import Button from '../common/Button.vue';
import InputText from '../common/InputText.vue';

export default {
    components: {
        Button,
        InputText
    },
    data() {
        return {
            regTitle: "Регистрация",
            formName: "",
            formMail: "",
            formPass: "",
            formPassConf: "",
            isRegistered: false
        }
    },
    methods: {
        ValidatePass() {
            if (this.formPass != this.formPassConf) {
                alert("Пароли не совпадают!");
                return false;
            }
            return true;
        },
        Register() {

            if (!this.ValidatePass()) {
                return;
            }

            this.$store.dispatch('auth/register', {name: this.formName, pass: this.formPass, mail: this.formMail}).then(() => {
                if (this.$store.getters['auth/status']) {
                    this.$router.push('/projects');
                }
                else {
                    alert("Регистрация не удалась!");
                    this.formName = "";
                    this.formPassConf = "";
                    this.formMail = "";
                    this.formPass = "";
                }
            });
        }
    },
    mounted() {
        this.$store.commit('auth/logout');
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            <div class="form">
                {{ this.regTitle }}
                <InputText v-model="this.formName" :placeholder="'Аккаунт'"/>
                <InputText v-model="this.formMail" :placeholder="'Почта'"/>
                <InputText v-model="this.formPass" :placeholder="'Пароль'"/>
                <InputText v-model="this.formPassConf" :placeholder="'Подтверждение пароля'"/>
            </div>
            <div class="form-btns">
                <Button class="log-btn first" :title="'Зарегистрироваться'" :func="this.Register"></Button>
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