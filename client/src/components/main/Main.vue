<script>
import { mapGetters } from 'vuex';
import Schedulers from './old/Schedules.vue'
import Clients from './old/Clients.vue'
import Stats from './old/Stats.vue'
import Employ from './old/Employ.vue';

export default {
    components: {
        Schedulers,
        Clients,
        Stats,
        Employ
    },
    data() {
        return {
            funcSA: "Расписание занятий",
            funcS: "Абонемент",
            funcCl: "Клиенты",
            funcClR: "Записать клиента",
            funcSO: "Личное расписание",
            funcClA: "Регистрация клиента",
            funcSt: "Статистика",
            funcStaff: "Персонал",
            funcServ: "Услуги",
            activeMenuNumber: -1,
            showContent: [false, false, false, false, false, false, false],
            showButtons: [true, true, true, true, true, true, true, true, true]
        }
    },
    methods: {

        switchStyleMenu(id) {
           
            this.showContent[this.activeMenuNumber] = false;
            this.showContent[id] = true;

            var nodes = document.getElementById('funcList').childNodes;
            if (this.activeMenuNumber != -1) {
                nodes[this.activeMenuNumber].firstChild.style.backgroundColor = "";
            }
            nodes[id].firstChild.style.backgroundColor = "rgb(70, 70, 70)";

            this.activeMenuNumber = id;
        },

        updateView() {

            const opt = this.option;

            var nodes = document.getElementById('funcList').childNodes;
            if (this.activeMenuNumber != -1) {
                nodes[this.activeMenuNumber].firstChild.style.backgroundColor = "";
            }
            this.showContent[this.activeMenuNumber] = false;
            this.activeMenuNumber = -1;

            switch (opt) {
                case this.$store.state.listOpt[0]: //Все
                    this.showButtons = [true, true, true, true, true, true, true, true, true];
                    break;
                case this.$store.state.listOpt[2]: //Менеджер
                    this.showButtons = [false, false, false, false, false, false, false, true, true];
                    break;
                case this.$store.state.listOpt[3]: //Отдел продаж
                    this.showButtons = [false, false, false, false, false, true, true, false, false];
                    break;
                case this.$store.state.listOpt[4]: //Тренер
                    this.showButtons = [false, false, false, false, true, false, false, false, false];
                    break;
                case this.$store.state.listOpt[5]: //Ресепшн
                    this.showButtons = [false, false, true, true, false, false, false, false, false];
                    break;
                case this.$store.state.listOpt[1]: //Клиент
                    this.showButtons = [true, true, false, false, false, false, false, false, false];
                    break;
                default:
                    break;
            }
        }
    },
    watch: {
    option: {
        deep: true,
        handler(value) {
            return this.updateView();
        }
    }
    },
    computed: {
    ...mapGetters(["option"]),
    }
}

</script>

<template>
    <div class="main-wrapper">
        <div class="main-left">
            <div class="func-wrapper">
                <ul id="funcList" class="func-list">
                    <li v-if="showButtons[0]" class="func-item">
                        <button id="mSchedulesAll" class="func-btn" type="button" @click="switchStyleMenu(0)">
                            {{ funcSA }}
                        </button>
                    </li>
                    <li v-if="showButtons[1]" class="func-item">
                        <button id="mSubscription" class="func-btn" type="button" @click="switchStyleMenu(1)">
                            {{ funcS }}
                        </button>
                    </li>
                    <li v-if="showButtons[2]" class="func-item">
                        <button id="mClients" class="func-btn" @click="switchStyleMenu(2)">
                            {{ funcCl }}
                        </button>
                    </li>
                    <li v-if="showButtons[3]" class="func-item">
                        <button id="mClientReg" class="func-btn" @click="switchStyleMenu(3)">
                            {{ funcClR }}
                        </button>
                    </li>
                    <li v-if="showButtons[4]" class="func-item">
                        <button id="mSchedulesOne" class="func-btn" @click="switchStyleMenu(4)">
                            {{ funcSO }}
                        </button>
                    </li>
                    <li v-if="showButtons[5]" class="func-item">
                        <button id="mClientAdd" class="func-btn" @click="switchStyleMenu(5)">
                            {{ funcClA }}
                        </button>
                    </li>
                    <li v-if="showButtons[6]" class="func-item">
                        <button id="mStats" class="func-btn" @click="switchStyleMenu(6)">
                            {{ funcSt }}
                        </button>
                    </li>
                    <li v-if="showButtons[7]" class="func-item">
                        <button id="mStaff" class="func-btn" @click="switchStyleMenu(7)">
                            {{ funcStaff }}
                        </button>
                    </li>
                    <li v-if="showButtons[8]" class="func-item">
                        <button id="mServices" class="func-btn" @click="switchStyleMenu(8)">
                            {{ funcServ }}
                        </button>
                    </li>
                </ul>
            </div>
        </div>
        <div class="v-divider"></div>
        <div class="main-right">
            <div id="cContentList" class="content-wrapper">
                <Schedulers v-if="showContent[0]"/>
                <div v-if="showContent[1]">
                    PLACEHOLDER2
                </div>
                <Clients v-if="showContent[2]"/>
                <div v-if="showContent[3]">
                    PLACEHOLDER4
                </div>
                <div v-if="showContent[4]">
                    PLACEHOLDER5
                </div>
                <div v-if="showContent[5]">
                    PLACEHOLDER6
                </div>
                <Stats v-if="showContent[6]"/>
                <Employ v-if="showContent[7]"/>
                <div v-if="showContent[8]">
                    PLACEHOLDER9
                </div>
            </div>
        </div>
    </div>
</template>

<style>

.main-wrapper {
    display: flex;
    min-height: 92.8%;
    background-color: rgb(41, 41, 41);
}

.main-left {
    width: 20%;
}

.v-divider {
    background-color: rgb(74, 74, 74);
    width: 1px;
    margin-left: 0px;
    margin-right: 5px;
    margin-top: 0px;
    margin-bottom: 0px;
}

.main-right {
    width: 80%;
}

.content-wrapper {
    padding: 20px;
    height: 100%;
}

.func-wrapper {
    margin-top: 0px;
}

.content-disable {
    display: none;
}

.func-item {    
    margin-top: 0px;
    width: 100%;
    height: 50px;
}

.func-btn {
    display: block; 
    height: 100%; 
    width: 100%;
    border: 0px;
    font-size: 20px;
    color: rgb(226, 226, 226);
    background-color: rgb(58, 58, 58);
}

.func-btn:link, .func-btn:visited, .func-btn:focus {
    background: rgb(58, 58, 58);
}

.func-btn:hover {
    background: rgb(65, 65, 65);
}

.func-btn:active {
    background: rgb(63, 63, 63);
}

</style>