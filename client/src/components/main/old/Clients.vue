<script>
import Button from '../../../common/Button.vue'
import Table from '../../../common/Table.vue'
import HDivider from '../../../common/HDivider.vue'
import axios from 'axios'

export default {
    components: {
        Button,
        Table,
        HDivider
    },
    data() { 
        return {
            text: {
                buttonStat: "Узнать посещаемость",
                buttonAdd: "Добавить посещение",
                buttonBack: "Назад",
                formStatDate: "Дата",
                formStatTime: "Время",
                formStatSubmit: "Найти",
                formAddName: "Имя",
                formAddSurname: "Фамилия",
                formAddMidname: "Отчество",
                formAddDate: "Дата",
                formAddTime: "Время",
                formAddButton: "Внести",
            },
            showItem: {
                stat: false,
                add: false,
                table: false
            },
            stat: {
                date: null,
                time: null
            },
            add: {
                name: null,
                surname: null,
                midname: null,
                date: null,
                time: null
            },

            tableHead: [
                "Имя",
                "Фамилия",
                "Отчество",
                "Дата",
                "Время"
            ],
            tableInfo: [{
                name: "...",
                surname: "...",
                midname: "...",
                date: "...",
                time: "..."
            }],
        }
    },
    methods: {
        btnStat() {
            this.showItem.stat = true;
            return null;
        },        
        btnAdd() {
            this.showItem.add = true;
            return null;
        },
        btnBack() {
            this.showItem.stat = false;
            this.showItem.add = false;
            this.showItem.table = false;
            return null;
        },
        btnSubmitStat() {
            const path = 'http://localhost:5000/select1';
            axios.get(path)
                .then((res) => {
                console.log(res.data)
                this.msg = res.data;
                })
                .catch((error) => {
                console.error(error);
                });
            this.showItem.stat = false;
            this.showItem.table = true;
            return null;
        },
        btnSubmitAdd() {
            this.showItem.stat = false;
            this.showItem.table = false;
            this.showItem.add = false;
            return null;
        }
    }
}
</script>

<template>
<div v-if="!showItem.stat && !showItem.add && !showItem.table" class="btn-wrapper margin-2">
    <Button class="btn-size" :title="text.buttonAdd" :func="btnAdd"></Button>
    <Button class="btn-size" :title="text.buttonStat" :func="btnStat"></Button>
</div>

<div v-if="showItem.stat" class="form-wrapper margin-3">
    <form id="stat" @submit.prevent="btnSubmitStat" required>
        <p>
            <label for="date">{{ text.formStatDate }}</label>
            <input id="date" v-model="stat.date" placeholder="**.**.****">
        </p>
    </form>
    <HDivider></HDivider>
    <div>
        <Button class="btn-size" :title="text.buttonBack" :func="btnBack" form=""></Button>
        <Button class="btn-size" :title="text.formStatSubmit" form="stat"></Button>
    </div>
</div>

<div v-if="showItem.table">
    <Table :table-head="tableHead" :table-info="tableInfo" :back-func="btnBack" :upd-btn="false"></Table>
</div>

<div v-if="showItem.add" class="form-wrapper margin-1">
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
            <label for="time">{{ text.formAddTime }}</label>
            <input id="time" v-model="add.time" placeholder="...">
        </p>
        <HDivider></HDivider>
        <p>
            <label for="date">{{ text.formAddDate }}</label>
            <input id="date" v-model="add.date" placeholder="...">
        </p>
        <HDivider></HDivider>
    </form>
    <div>
        <Button class="btn-size" :title="text.buttonBack" :func="btnBack"></Button>
        <Button class="btn-size" :title="text.formAddButton" form="add"></Button>
    </div>
</div>

</template>

<style scoped>

form p {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

label {
    font-size: 20px;
}

.div-wrapper div, .stat-wrapper div {
    display: flex;
    margin: 10px;
    justify-content: space-evenly;
}

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