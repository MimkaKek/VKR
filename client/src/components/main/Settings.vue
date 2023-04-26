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
            type: "",
            projectName: "",
            projectDesc: "",
            projectTemp: "",
            isPublic: false,
            isTemplate: false,
            formPass: "",
        }
    },
    methods: {
        changePublic() {
            this.isPublic = this.isPublic ? false : true;
            return null;
        },
        changeTemplate() {
            this.isTemplate = this.isTemplate ? false : true;
            return null;
        },

    },
    mounted() {
        
    }
}

</script>

<template>
    <div class="main">
        <div class="box">
            <InputText v-model="projectName" :placeholder="'Название...'"/>
            <InputText v-model="projectDesc" :textarea="true" :placeholder="'Описание...'"/>
            <div class="menu-btn">
                <Button :title="isPublic ? 'Публичный' : 'Закрытый'" :func="this.changePublic"></Button>
                <div class="space"></div>
                <Button :title="isTemplate ? 'Шаблон' : 'Проект'" :func="this.changeTemplate"></Button>
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