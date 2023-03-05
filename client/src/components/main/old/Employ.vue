<script>
import axios from 'axios';
import Button from '../../../common/Button.vue';
import HDivider from '../../../common/HDivider.vue';
import Table from '../../../common/Table.vue';

export default {
    components: {
        Button,
        HDivider,
        Table
    },
    data() {
        return {
            msg: null,
            showItem: {
                add: false,
                success: false,
                remove: false
            },
            text: {
                buttonAdd: "Новый сотрудник",
                buttonRemove: "Удалить сотрудника",
                buttonBack: "Назад",
                formAddName: "Имя",
                formAddSurname: "Фамилия",
                formAddMidname: "Отчество",
                formAddJob: "ID должности",
                formAddButton: "Добавить"
            },
            add: {
                name: null,
                surname: null,
                midname: null,
                job_id: null,
            },
        }
    },
    methods: {
        btnAdd() {
            this.showItem.add = true;
        },
        btnBack() {
            this.showItem.add = false;
            this.showItem.success = false;
            this.showItem.remove = false;
        },
        btnSubmitAdd() {
            const path = 'http://localhost:5000/insert-employee?name=' + this.add.name + '&surname=' + this.add.surname + '&patronymic=' + this.add.midname + "&job=" + this.add.job_id; //http://127.0.0.1:5000/insert-employee?name=&surname=&patronymic=&job=
            axios.post(path)
                .then((res) => {
                    console.log(res.data);
                    this.msg = res.data;
                    this.showItem.add = false;
                    this.showItem.success = true;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnRemove() {
            const path = 'http://localhost:5000//get-employee-data'
            axios.get(path)
                .then((res) => {
                    console.log(res.data);
                    this.input = res.data.split("|");
                    this.tableHead = {
                        id: "ID",
                        surname: "Фамилия",
                        name: "Имя",
                        midname: "Отчество"
                    }
                    this.tableInfo = []
                    for(var i = 0; i < this.input.length - 1; i++) {
                        this.input[i] = this.input[i].trim();
                        var tmpStr = this.input[i].split(" ");
                        var tmpObj = {
                            id: tmpStr[0],
                            surname: tmpStr[1],
                            name: tmpStr[2],
                            midname: tmpStr[3]
                        }
                        this.tableInfo.push(tmpObj);
                    }
                    this.showItem.remove = true;
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    }
}

</script>

<template>
<div v-if="!showItem.add && !showItem.success && !showItem.remove" class="btn-wrapper margin-2">
    <Button class="btn-size" :title="text.buttonAdd" :func="btnAdd"></Button>
    <Button class="btn-size" :title="text.buttonRemove" :func="btnRemove"></Button>
</div>

<div v-if="showItem.add" class="btn-wrapper margin-1">
    <form id="add" @submit.prevent="btnSubmitAdd">
        <p>
            <label for="name">{{ text.formAddName }}</label>
            <input id="name" v-model="add.name" placeholder="...">
        </p>
        <HDivider></HDivider>
        <p>
            <label for="surname">{{ text.formAddSurname }}</label>
            <input id="surname" v-model="add.surname" placeholder="...">
        </p>
        <HDivider></HDivider>
        <p>
            <label for="midname">{{ text.formAddMidname }}</label>
            <input id="midname" v-model="add.midname" placeholder="...">
        </p>
        <HDivider></HDivider>
        <p>
            <label for="jobid">{{ text.formAddJob }}</label>
            <input id="jobid" v-model="add.job_id" placeholder="...">
        </p>
        <HDivider></HDivider>
    </form>
    <div>
        <Button class="btn-size" :title="text.buttonBack" :func="btnBack"></Button>
        <Button class="btn-size" :title="text.formAddButton" form="add"></Button>
    </div>
</div>

<div v-if="showItem.success" class="btn-wrapper margin-3">
    <HDivider></HDivider>
    Успех!
    <HDivider></HDivider>
    <Button class="btn-size" :title="text.buttonBack" :func="btnBack"></Button>
</div>

<div v-if="showItem.remove">
    <Table :back-func="btnBack" :upd-btn="false"></Table>
</div>
</template>

<style scoped>

.form-wrapper div button, .btn-wrapper div button, form .btn-size, table div .btn-size {
    width: auto;
}

input {
    width:200px;
    padding:10px;
    margin-left: 10px;
    border-radius: 10px;
    border: 1px;
    background-color: rgb(60,60,60);
    font-size: 20px;
    color: rgb(226, 226, 226);
}

.btn-size {
    padding: 20px
}

.form-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.margin-1 {
    margin-top: 15%;
}

.margin-2 {
    margin-top: 20%;
}

.margin-3 {
    margin-top: 22%;
}

.btn-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

</style>