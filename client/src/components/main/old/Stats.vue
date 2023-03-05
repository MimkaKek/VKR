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
                buttonFit: "Работающие тренера",
                buttonFitPop: "Популярные тренера",
                buttonFitUnPop: "Непопулярные тренера",
                buttonSecPop: "Популярные занятия",
                buttonSecUnPop: "Непопулярные занятия",
                buttonMon: "Данные по зарплате",
                buttonClients: "Клиенты в зоне риска",
                buttonBack: "Назад",
                buttonDate: "Дата",
                formStatSubmit: "Найти"
            },
            showItem: {
                Fit: false,
                FitPop: false,
                FitUnPop: false,
                SecPop: false,
                SecUnPop: false,
                Mon: false,
                Clients: false,
                Back: false,
                All: true
            },
            input: null,
            out: {
                date: null
            },
            tableHead: [
                "Имя",
                "Фамилия",
                "Отчество",
                "Дата",
                "Время"
            ],
            tableInfo: [{
                name: "Имя 1",
                surname: "Фамилия 1",
                midname: "Отчество 1",
                date: "01.12.2022",
                time: "15:30"
            }, 
            {
                name: "Имя 2",
                surname: "Фамилия 2",
                midname: "Отчество 2",
                date: "01.12.2022",
                time: "15:45"
            }],
        }
    },
    methods: {
        btnFit() {
            this.showItem.Fit = true;
            this.showItem.All = false;
        },
        btnFitPop() {
            const path = 'http://localhost:5000/select3';
            axios.get(path)
                .then((res) => {
                    this.input = res.data.split("|")[0].split(" ");
                    this.showItem.FitPop = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnFitUnPop() {
            const path = 'http://localhost:5000/select4';
            axios.get(path)
                .then((res) => {
                    this.input = res.data.split("|")[0].split(" ");
                    this.showItem.FitUnPop = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnSecPop() {
            const path = 'http://localhost:5000/select5';
            axios.get(path)
                .then((res) => {
                    this.input = res.data.split("|")[0];
                    this.showItem.SecPop = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnSecUnPop() {
            const path = 'http://localhost:5000/select6';
            axios.get(path)
                .then((res) => {
                    this.input = res.data.split("|")[0];
                    this.showItem.SecUnPop = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
            
        },
        btnMon() {
            const path = 'http://localhost:5000/select7';
            axios.get(path)
                .then((res) => {
                    this.input = res.data.split("|");
                    this.tableHead = {
                        surname: "Фамилия",
                        name: "Имя",
                        midname: "Отчество",
                        date: "Дата",
                        time: "Время"
                    }
                    this.tableInfo = []
                    for(var i = 0; i < this.input.length - 1; i++) {
                        this.input[i] = this.input[i].trim();
                        var tmpStr = this.input[i].split(" ");
                        var tmpObj = {
                            surname: tmpStr[0],
                            name: tmpStr[1],
                            midname: tmpStr[2],
                            date: tmpStr[3],
                            time: tmpStr[4]
                        }
                        this.tableInfo.push(tmpObj);
                    }
                    this.showItem.Mon = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnClients() {
            const path = 'http://localhost:5000/select8';
            axios.get(path)
                .then((res) => {
                    this.input = res.data;

                    this.input = res.data.split("|");
                    this.tableHead = {
                        surname: "Фамилия",
                        name: "Имя",
                        midname: "Отчество",
                        date1: "Дата записи",
                        time1: "Время записи",
                        date2: "Дата окончания"
                    }
                    this.tableInfo = [];
                    for(var i = 0; i < this.input.length - 1; i++) {
                        this.input[i] = this.input[i].trim();
                        var tmpStr = this.input[i].split(" ");
                        var tmpObj = {
                            surname: tmpStr[0],
                            name: tmpStr[1],
                            midname: tmpStr[2],
                            date1: tmpStr[4],
                            time2: tmpStr[5],
                            date2: tmpStr[6]
                        }
                        this.tableInfo.push(tmpObj);
                    }

                    this.showItem.Clients = true;
                    this.showItem.All = false;
                })
                .catch((error) => {
                    console.error(error);
                });
        },
        btnBack() {
            this.showItem = {
                Fit: false,
                FitPop: false,
                FitUnPop: false,
                SecPop: false,
                SecUnPop: false,
                Mon: false,
                Clients: false,
                Back: false,
                All: true
            };
        },
        btnSubmitStat() {
            console.log("Submit form!");
            return null;
        }
    }
}
</script>

<template>
<div v-if="showItem.All" class="btn-menu">
    <Button :title="text.buttonFit" :func="btnFit"></Button>
    <Button :title="text.buttonFitPop" :func="btnFitPop"></Button>
    <Button :title="text.buttonFitUnPop" :func="btnFitUnPop"></Button>
    <Button :title="text.buttonSecPop" :func="btnSecPop"></Button>
    <Button :title="text.buttonSecUnPop" :func="btnSecUnPop"></Button>
    <Button :title="text.buttonMon" :func="btnMon"></Button>
    <Button :title="text.buttonClients" :func="btnClients"></Button>
</div>

<div v-if="showItem.Fit" class="form-wrapper margin-3">
    <form id="fitStat" @submit.prevent="btnSubmitStat">
        <p>
            <label for="date">{{ text.buttonDate }}</label>
            <input id="date" v-model="out.date" placeholder="****-**-**">
        </p>
    </form>
    <HDivider></HDivider>
    <div>
        <Button class="btn-size" :title="text.buttonBack" :func="btnBack" form=""></Button>
        <Button class="btn-size" :title="text.formStatSubmit" form="fitStat"></Button>
    </div>
</div>

<div v-if="showItem.FitPop">
    Самый популярный тренер - {{ input[0] }} {{ input[1] }} {{ input[2] }}
    <HDivider></HDivider>
    <Button :title="text.buttonBack" :func="btnBack"></Button>
</div>

<div v-if="showItem.FitUnPop">
    Самый не популярный тренер - {{ input[0] }} {{ input[1] }} {{ input[2] }}
    <HDivider></HDivider>
    <Button :title="text.buttonBack" :func="btnBack"></Button>
</div>

<div v-if="showItem.SecPop">
    Популярное занятие - {{ input }}
    <HDivider></HDivider>
    <Button :title="text.buttonBack" :func="btnBack"></Button>
</div>

<div v-if="showItem.SecUnPop">
    Не популярное занятие - {{ input }}
    <HDivider></HDivider>
    <Button :title="text.buttonBack" :func="btnBack"></Button>
</div>

<div v-if="showItem.Mon">
    <Table :back-func="btnBack" :update-func="btnMon" :table-head="tableHead" :table-info="tableInfo"></Table>
</div>

<div v-if="showItem.Clients">
    <Table :back-func="btnBack" :update-func="btnClients" :table-head="tableHead" :table-info="tableInfo"></Table>
</div>

</template>

<style scoped>

.btn-menu {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 20%;
}

form p {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

label {
    font-size: 20px;
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

</style>